import csv
import json
import random
from datetime import datetime, timezone
from io import BytesIO, StringIO
import uuid
import zipfile

from flask import Blueprint, Response, current_app, jsonify, request, send_file
from flask_login import current_user

from config import Config
from extensions import db
from models import FarmTask, PestScan, Plot, SensorReading, SoilReport
from services.chatbot_service import generate_chat_reply
from services.crop_calendar import get_crop_stages
from services.fertilizer_guide import get_fertilizer_guide
from services.ml_service import (
    analyze_soil_sample,
    get_dataset_explorer,
    get_model_insights,
    recommend_crops_prototype,
    validate_soil_payload,
)
from services.pdf_service import (
    build_comparison_pdf,
    build_sample_bag_tag_pdf,
    build_soil_report_pdf,
)
from services.pest_vision_service import analyze_pest_image, get_pest_reference_guide
from services.weather_service import fetch_weather

api_bp = Blueprint("api", __name__, url_prefix="/api")

_MAX_BATCH_BYTES = 1024 * 1024
_MAX_BATCH_ROWS = 100


def _scoped_reports_query():
    if current_user.is_authenticated:
        return SoilReport.query.filter_by(user_id=current_user.id)
    return SoilReport.query.filter(SoilReport.user_id.is_(None))


def _scoped_plots_query():
    if current_user.is_authenticated:
        return Plot.query.filter_by(user_id=current_user.id)
    return Plot.query.filter(Plot.user_id.is_(None))


def _csv_safe(val) -> str:
    text = "" if val is None else str(val)
    if text and text[0] in ("=", "+", "-", "@", "\t", "\r"):
        return "'" + text
    return text


def _sync_legacy_history_file(report: SoilReport) -> None:
    try:
        try:
            with open(Config.LEGACY_HISTORY_PATH, "r", encoding="utf-8") as fh:
                existing = json.load(fh)
            if not isinstance(existing, list):
                existing = []
        except (OSError, ValueError):
            existing = []

        existing.insert(0, {
            "report_uid": report.report_uid,
            "crop": report.crop,
            "soil_type": report.soil_type,
            "score": report.score,
            "fertilizer": report.fertilizer,
            "summary": report.summary,
            "date": report.display_date,
        })
        with open(Config.LEGACY_HISTORY_PATH, "w", encoding="utf-8") as fh:
            json.dump(existing[:100], fh, indent=2)
    except OSError:
        current_app.logger.warning("Could not update legacy history.json")


def _resolve_plot(plot_id_raw) -> Plot | None:
    if plot_id_raw in (None, "", "none"):
        return None
    try:
        pid = int(plot_id_raw)
    except (TypeError, ValueError) as exc:
        raise ValueError("Invalid plot selection.") from exc
    plot = _scoped_plots_query().filter(Plot.id == pid).first()
    if not plot:
        raise ValueError("Selected field plot was not found.")
    return plot


def _save_report(inputs: dict, result: dict, plot: Plot | None = None, source: str = "analysis") -> SoilReport:
    now_local = datetime.now()
    display_date = now_local.strftime("%d %b %Y, %I:%M %p")
    report_uid = f"AN-{now_local.strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

    report = SoilReport(
        report_uid=report_uid,
        user_id=current_user.id if current_user.is_authenticated else None,
        plot_id=plot.id if plot else None,
        plot_name=plot.name if plot else None,
        crop=inputs["crop"],
        soil_type=inputs["soil_type"],
        temperature=inputs["temperature"],
        humidity=inputs["humidity"],
        moisture=inputs["moisture"],
        nitrogen=inputs["nitrogen"],
        phosphorus=inputs["phosphorus"],
        potassium=inputs["potassium"],
        ph=inputs["ph"],
        score=result["score"],
        fertilizer=result["fertilizer"],
        summary=result["summary"],
        gaps_json=json.dumps(result["gaps"]),
        health_json=json.dumps(result["health"]),
        actions_json=json.dumps(result["actions"]),
        probs_json=json.dumps(result.get("tree_vote_distribution") or []),
        disclaimer=result["disclaimer"],
        source=source,
        display_date=display_date,
        created_at=datetime.now(timezone.utc),
    )
    db.session.add(report)
    db.session.commit()

    if not current_user.is_authenticated and source == "analysis":
        _sync_legacy_history_file(report)

    return report


@api_bp.get("/health")
def health_check():
    return jsonify({"status": "ok", "app": "Agri Nova AI"}), 200


@api_bp.get("/model-insights")
def model_insights():
    return jsonify(get_model_insights()), 200


@api_bp.get("/dashboard")
def dashboard_summary():
    plot_id = request.args.get("plot_id", "").strip()
    query = _scoped_reports_query()
    if plot_id and plot_id != "all":
        try:
            query = query.filter(SoilReport.plot_id == int(plot_id))
        except ValueError:
            pass

    reports = query.order_by(SoilReport.created_at.desc(), SoilReport.id.desc()).all()
    total = len(reports)
    latest = reports[0].to_dict(include_details=True) if reports else None

    crop_counts: dict[str, int] = {}
    fert_counts: dict[str, int] = {}
    for rep in reports:
        crop_counts[rep.crop] = crop_counts.get(rep.crop, 0) + 1
        fert_label = rep.fertilizer or "Not recorded"
        fert_counts[fert_label] = fert_counts.get(fert_label, 0) + 1

    trend_reports = list(reversed(reports[:15]))
    trend_series = [
        {
            "id": r.id,
            "report_uid": r.report_uid,
            "label": f"{r.crop} ({r.display_date.split(',')[0]})" if r.display_date else r.crop,
            "score": r.score,
            "crop": r.crop,
            "fertilizer": r.fertilizer,
            "nitrogen": r.nitrogen,
            "phosphorus": r.phosphorus,
            "potassium": r.potassium,
            "ph": r.ph,
        }
        for r in trend_reports
    ]

    tips = [
        {
            "title": "Test Soil Before Every Season",
            "detail": "Laboratory soil tests help avoid over-applying nitrogen or phosphorus and protect groundwater.",
        },
        {
            "title": "Check Soil pH First",
            "detail": "Even when NPK is present, extreme soil pH can lock up phosphorus and micronutrients.",
        },
        {
            "title": "Match Moisture to Soil Texture",
            "detail": "Sandy soils drain quickly while clayey and black soils hold water longer—adjust irrigation accordingly.",
        },
        {
            "title": "Combine Organic & Mineral Care",
            "detail": "Compost and crop residues improve soil organic matter, structure, and microbial resilience.",
        },
    ]

    return jsonify({
        "total_analyses": total,
        "reports_generated": total,
        "latest_analysis": latest,
        "recent_history": [r.to_dict(include_details=False) for r in reports[:6]],
        "trend_series": trend_series,
        "crop_distribution": crop_counts,
        "fertilizer_distribution": fert_counts,
        "plots_count": _scoped_plots_query().count(),
        "supported_crops": list(Config.CROP_MAPPING.keys()),
        "supported_soils": Config.ALLOWED_SOILS,
        "tips": tips,
        "server_date": datetime.now().strftime("%A, %d %B %Y"),
    }), 200


@api_bp.post("/analyze")
def analyze():
    try:
        data = request.get_json(silent=True)
        if data is None:
            return jsonify(error="Invalid JSON payload."), 400

        plot = _resolve_plot(data.get("plot_id"))
        inputs, result = analyze_soil_sample(data)
        report = _save_report(inputs, result, plot=plot, source="analysis")

        result["report_id"] = report.id
        result["report_uid"] = report.report_uid
        result["plot_id"] = report.plot_id
        result["plot_name"] = report.plot_name or ""
        result["date"] = report.display_date
        result["inputs"] = {**inputs, "plot_name": report.plot_name or ""}

        return jsonify(result), 200

    except ValueError as error:
        return jsonify(error=str(error)), 400
    except Exception:
        current_app.logger.exception("Soil analysis prediction failed")
        return jsonify(error="Prediction failed. Check the model and server logs."), 500


@api_bp.post("/analyze/simulate")
def simulate_soil():
    """Run live What-If sensitivity check without saving to history."""
    try:
        data = request.get_json(silent=True)
        if data is None:
            return jsonify(error="Invalid JSON payload."), 400
        inputs, result = analyze_soil_sample(data)
        result["is_simulation"] = True
        result["inputs"] = inputs
        return jsonify(result), 200
    except ValueError as error:
        return jsonify(error=str(error)), 400
    except Exception:
        current_app.logger.exception("Simulation failed")
        return jsonify(error="Simulation failed."), 500


@api_bp.get("/batch/template")
def batch_csv_template():
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "crop", "soil_type", "temperature", "humidity", "moisture",
        "nitrogen", "phosphorus", "potassium", "ph",
    ])
    writer.writerow(["Rice", "Clayey", "28", "68", "52", "36", "14", "18", "6.2"])
    writer.writerow(["Wheat", "Loamy", "24", "55", "44", "22", "42", "30", "6.8"])
    writer.writerow(["Cotton", "Black", "31", "62", "58", "18", "34", "28", "7.1"])
    return Response(
        output.getvalue(),
        mimetype="text/csv; charset=utf-8",
        headers={"Content-Disposition": "attachment; filename=agri_nova_batch_template.csv"},
    )


@api_bp.post("/batch/analyze")
def batch_analyze_csv():
    file = request.files.get("file")
    if not file or not file.filename:
        return jsonify(error="Please select a .csv file to upload."), 400
    if not file.filename.lower().endswith(".csv"):
        return jsonify(error="Only .csv files are supported."), 400

    raw_bytes = file.read(_MAX_BATCH_BYTES + 1)
    if len(raw_bytes) > _MAX_BATCH_BYTES:
        return jsonify(error="CSV file exceeds the 1 MB upload limit."), 400
    if not raw_bytes:
        return jsonify(error="Uploaded CSV file is empty."), 400

    try:
        text_content = raw_bytes.decode("utf-8-sig")
    except UnicodeDecodeError:
        return jsonify(error="CSV file must be UTF-8 encoded."), 400

    reader = csv.DictReader(StringIO(text_content))
    if not reader.fieldnames:
        return jsonify(error="CSV header row is missing."), 400

    normalized_fields = {f.strip().lower(): f for f in reader.fieldnames if f}
    required = {
        "crop", "soil_type", "temperature", "humidity", "moisture",
        "nitrogen", "phosphorus", "potassium", "ph",
    }
    missing = sorted(required - set(normalized_fields.keys()))
    if missing:
        return jsonify(
            error=f"Missing required CSV columns: {', '.join(missing)}. Download the template for reference."
        ), 400

    save_to_history = str(request.form.get("save_to_history", "false")).lower() in ("true", "1", "yes")
    plot = None
    try:
        plot = _resolve_plot(request.form.get("plot_id"))
    except ValueError as err:
        return jsonify(error=str(err)), 400

    results = []
    errors = []
    rows_processed = 0

    for row_num, raw_row in enumerate(reader, start=2):
        if rows_processed >= _MAX_BATCH_ROWS:
            errors.append({"row": row_num, "error": f"Stopped after {_MAX_BATCH_ROWS} rows (prototype batch cap)."})
            break
        rows_processed += 1

        clean_row = {
            norm_key: (raw_row.get(orig_key) or "").strip()
            for norm_key, orig_key in normalized_fields.items()
        }
        try:
            inputs, res = analyze_soil_sample(clean_row)
            saved_uid = ""
            if save_to_history:
                rep = _save_report(inputs, res, plot=plot, source="batch_csv")
                saved_uid = rep.report_uid
            results.append({
                "row": row_num,
                "report_uid": saved_uid,
                "crop": inputs["crop"],
                "soil_type": inputs["soil_type"],
                "nitrogen": inputs["nitrogen"],
                "phosphorus": inputs["phosphorus"],
                "potassium": inputs["potassium"],
                "ph": inputs["ph"],
                "moisture": inputs["moisture"],
                "fertilizer": res["fertilizer"],
                "score": res["score"],
                "health_overall": res["health"]["overall"],
            })
        except ValueError as err:
            errors.append({"row": row_num, "error": str(err)})

    return jsonify({
        "processed": rows_processed,
        "succeeded": len(results),
        "failed": len(errors),
        "saved_to_history": save_to_history,
        "results": results,
        "errors": errors,
    }), 200


@api_bp.get("/plots")
def list_plots():
    plots = _scoped_plots_query().order_by(Plot.created_at.desc(), Plot.id.desc()).all()
    items = []
    for p in plots:
        d = p.to_dict()
        q = _scoped_reports_query().filter(SoilReport.plot_id == p.id)
        d["report_count"] = q.count()
        latest = q.order_by(SoilReport.created_at.desc(), SoilReport.id.desc()).first()
        d["latest_score"] = latest.score if latest else None
        d["latest_crop"] = latest.crop if latest else None
        d["latest_fertilizer"] = latest.fertilizer if latest else None
        items.append(d)
    return jsonify({"plots": items}), 200


@api_bp.post("/plots")
def create_plot():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    soil_type = str(data.get("soil_type", "Loamy")).strip()
    location = str(data.get("location", "")).strip()
    notes = str(data.get("notes", "")).strip()
    area_raw = data.get("area_acres")
    lat_raw = data.get("latitude")
    lon_raw = data.get("longitude")

    if not name or len(name) > 80:
        return jsonify(error="Plot name is required (max 80 characters)."), 400
    if soil_type not in Config.ALLOWED_SOILS:
        return jsonify(error="Select a valid soil type."), 400

    area_val = None
    if area_raw not in (None, ""):
        try:
            area_val = round(float(area_raw), 2)
            if area_val < 0 or area_val > 100000:
                return jsonify(error="Area must be between 0 and 100,000 acres."), 400
        except (TypeError, ValueError):
            return jsonify(error="Area must be a valid number."), 400

    lat_val, lon_val = None, None
    if lat_raw not in (None, "") or lon_raw not in (None, ""):
        try:
            lat_val = round(float(lat_raw), 6)
            lon_val = round(float(lon_raw), 6)
            if not (-90 <= lat_val <= 90 and -180 <= lon_val <= 180):
                return jsonify(error="Latitude must be -90..90 and longitude -180..180."), 400
        except (TypeError, ValueError):
            return jsonify(error="Latitude and longitude must be valid numbers."), 400

    plot = Plot(
        user_id=current_user.id if current_user.is_authenticated else None,
        name=name,
        soil_type=soil_type,
        location=location[:120],
        area_acres=area_val,
        latitude=lat_val,
        longitude=lon_val,
        notes=notes[:255],
    )
    db.session.add(plot)
    db.session.commit()
    return jsonify({"plot": plot.to_dict()}), 201


@api_bp.delete("/plots/<int:plot_id>")
def delete_plot(plot_id: int):
    plot = _scoped_plots_query().filter(Plot.id == plot_id).first()
    if not plot:
        return jsonify(error="Plot not found."), 404
    db.session.delete(plot)
    db.session.commit()
    return jsonify({"deleted": True, "id": plot_id}), 200


@api_bp.post("/crop-recommend")
def crop_recommend():
    try:
        data = request.get_json(silent=True)
        if data is None:
            return jsonify(error="Invalid JSON payload."), 400
        recommendation = recommend_crops_prototype(data)
        return jsonify(recommendation), 200
    except ValueError as error:
        return jsonify(error=str(error)), 400
    except Exception:
        current_app.logger.exception("Crop recommendation failed")
        return jsonify(error="Could not compute crop recommendation."), 500


@api_bp.get("/fertilizers")
def fertilizer_guide():
    search = request.args.get("q", "")
    nutrient = request.args.get("nutrient", "all")
    items = get_fertilizer_guide(search=search, nutrient=nutrient)
    return jsonify({"items": items, "count": len(items)}), 200


@api_bp.get("/weather")
def weather():
    city = request.args.get("city", "Bengaluru")
    lat_raw = request.args.get("lat")
    lon_raw = request.args.get("lon")
    lat, lon = None, None
    if lat_raw is not None and lon_raw is not None:
        try:
            lat = float(lat_raw)
            lon = float(lon_raw)
        except ValueError:
            return jsonify(error="Invalid latitude/longitude values."), 400
    payload, status_code = fetch_weather(city, lat=lat, lon=lon)
    return jsonify(payload), status_code


@api_bp.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", ""))

    latest_ctx = data.get("latest_analysis")
    if not isinstance(latest_ctx, dict) or not latest_ctx.get("crop"):
        latest_report = (
            _scoped_reports_query()
            .order_by(SoilReport.created_at.desc(), SoilReport.id.desc())
            .first()
        )
        latest_ctx = latest_report.to_dict(include_details=True) if latest_report else None

    reply_payload = generate_chat_reply(message, latest_analysis=latest_ctx)
    return jsonify(reply_payload), 200


@api_bp.get("/history")
def get_history():
    query = _scoped_reports_query()

    crop_filter = request.args.get("crop", "").strip()
    if crop_filter and crop_filter.lower() != "all":
        query = query.filter(SoilReport.crop == crop_filter)

    plot_filter = request.args.get("plot_id", "").strip()
    if plot_filter and plot_filter.lower() != "all":
        try:
            query = query.filter(SoilReport.plot_id == int(plot_filter))
        except ValueError:
            pass

    search_q = request.args.get("q", "").strip().lower()
    sort = request.args.get("sort", "newest").strip().lower()

    if sort == "oldest":
        query = query.order_by(SoilReport.created_at.asc(), SoilReport.id.asc())
    elif sort == "score_desc":
        query = query.order_by(SoilReport.score.desc(), SoilReport.id.desc())
    elif sort == "score_asc":
        query = query.order_by(SoilReport.score.asc(), SoilReport.id.desc())
    else:
        query = query.order_by(SoilReport.created_at.desc(), SoilReport.id.desc())

    reports = query.all()
    if search_q:
        reports = [
            r for r in reports
            if search_q in (r.crop or "").lower()
            or search_q in (r.fertilizer or "").lower()
            or search_q in (r.soil_type or "").lower()
            or search_q in (r.plot_name or "").lower()
            or search_q in (r.report_uid or "").lower()
            or search_q in (r.display_date or "").lower()
        ]

    return jsonify([r.to_dict(include_details=True) for r in reports[:100]]), 200


@api_bp.get("/history/compare")
def compare_history():
    ids_raw = request.args.get("ids", "")
    ids = []
    for part in ids_raw.split(","):
        part = part.strip()
        if part.isdigit():
            ids.append(int(part))
    ids = list(dict.fromkeys(ids))[:4]
    if len(ids) < 2:
        return jsonify(error="Select at least 2 reports to compare."), 400

    reports = _scoped_reports_query().filter(SoilReport.id.in_(ids)).all()
    by_id = {r.id: r.to_dict(include_details=True) for r in reports}
    ordered = [by_id[i] for i in ids if i in by_id]
    if len(ordered) < 2:
        return jsonify(error="Matching reports were not found."), 404
    return jsonify({"reports": ordered}), 200


@api_bp.get("/history/compare/pdf")
def compare_history_pdf():
    ids_raw = request.args.get("ids", "")
    ids = [int(p.strip()) for p in ids_raw.split(",") if p.strip().isdigit()]
    ids = list(dict.fromkeys(ids))[:4]
    if len(ids) < 2:
        return jsonify(error="Select at least 2 reports to compare."), 400

    reports = _scoped_reports_query().filter(SoilReport.id.in_(ids)).all()
    by_id = {r.id: r.to_dict(include_details=True) for r in reports}
    ordered = [by_id[i] for i in ids if i in by_id]
    if len(ordered) < 2:
        return jsonify(error="Matching reports were not found."), 404

    try:
        buf = build_comparison_pdf(ordered)
        return send_file(
            buf,
            mimetype="application/pdf",
            as_attachment=True,
            download_name="Agri_Nova_AI_Comparison_Report.pdf",
        )
    except Exception:
        current_app.logger.exception("Comparison PDF generation failed")
        return jsonify(error="Could not generate comparison PDF."), 500


@api_bp.get("/history/<int:report_id>")
def get_history_detail(report_id: int):
    report = _scoped_reports_query().filter(SoilReport.id == report_id).first()
    if not report:
        return jsonify(error="Report not found."), 404
    return jsonify(report.to_dict(include_details=True)), 200


@api_bp.delete("/history/<int:report_id>")
def delete_history_item(report_id: int):
    report = _scoped_reports_query().filter(SoilReport.id == report_id).first()
    if not report:
        return jsonify(error="Report not found."), 404
    db.session.delete(report)
    db.session.commit()
    return jsonify({"deleted": True, "id": report_id}), 200


@api_bp.delete("/history/clear")
def clear_history():
    deleted_count = _scoped_reports_query().delete(synchronize_session=False)
    db.session.commit()
    return jsonify({"cleared": True, "deleted_count": deleted_count}), 200


@api_bp.get("/history/export/csv")
def export_history_csv():
    reports = (
        _scoped_reports_query()
        .order_by(SoilReport.created_at.desc(), SoilReport.id.desc())
        .all()
    )
    if not reports:
        return jsonify(error="No reports available to export."), 404

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Report ID",
        "Date",
        "Plot",
        "Crop",
        "Soil Type",
        "Fertilizer Prediction",
        "Demo Soil Match Index",
        "Nitrogen (kg/ha)",
        "Phosphorus (kg/ha)",
        "Potassium (kg/ha)",
        "Soil pH",
        "Moisture (%)",
        "Temperature (C)",
        "Humidity (%)",
        "Summary",
    ])
    for r in reports:
        writer.writerow([
            _csv_safe(r.report_uid),
            _csv_safe(r.display_date),
            _csv_safe(r.plot_name or ""),
            _csv_safe(r.crop),
            _csv_safe(r.soil_type),
            _csv_safe(r.fertilizer),
            _csv_safe(r.score),
            _csv_safe(r.nitrogen),
            _csv_safe(r.phosphorus),
            _csv_safe(r.potassium),
            _csv_safe(r.ph),
            _csv_safe(r.moisture),
            _csv_safe(r.temperature),
            _csv_safe(r.humidity),
            _csv_safe(r.summary),
        ])

    return Response(
        output.getvalue(),
        mimetype="text/csv; charset=utf-8",
        headers={"Content-Disposition": "attachment; filename=agri_nova_ai_reports.csv"},
    )


@api_bp.post("/report/pdf")
def download_pdf_from_payload():
    try:
        data = request.get_json(silent=True) or {}
        inputs = data.get("inputs") or {}
        result = data.get("result") or {}
        if not inputs or not result:
            return jsonify(error="Analysis data is missing."), 400

        buffer = build_soil_report_pdf(
            inputs=inputs,
            result=result,
            report_uid=str(result.get("report_uid", "")),
        )
        return send_file(
            buffer,
            mimetype="application/pdf",
            as_attachment=True,
            download_name="Agri_Nova_AI_Soil_Report.pdf",
        )
    except Exception:
        current_app.logger.exception("PDF generation failed")
        return jsonify(error="Could not generate PDF report."), 500


@api_bp.get("/report/pdf/<int:report_id>")
def download_pdf_by_id(report_id: int):
    report = _scoped_reports_query().filter(SoilReport.id == report_id).first()
    if not report:
        return jsonify(error="Report not found."), 404

    rep = report.to_dict(include_details=True)
    inputs = {
        "crop": rep["crop"],
        "soil_type": rep["soil_type"],
        "plot_name": rep.get("plot_name", ""),
        "temperature": rep["temperature"],
        "humidity": rep["humidity"],
        "moisture": rep["moisture"],
        "nitrogen": rep["nitrogen"],
        "phosphorus": rep["phosphorus"],
        "potassium": rep["potassium"],
        "ph": rep["ph"],
    }
    try:
        buffer = build_soil_report_pdf(
            inputs=inputs,
            result=rep,
            report_uid=rep["report_uid"],
        )
        return send_file(
            buffer,
            mimetype="application/pdf",
            as_attachment=True,
            download_name=f"Agri_Nova_AI_{rep['report_uid']}.pdf",
        )
    except Exception:
        current_app.logger.exception("Historical PDF generation failed")
        return jsonify(error="Could not generate PDF report."), 500


@api_bp.get("/dataset-explorer")
def dataset_explorer():
    crop_f = request.args.get("crop", "all")
    fert_f = request.args.get("fertilizer", "all")
    try:
        return jsonify(get_dataset_explorer(crop_filter=crop_f, fertilizer_filter=fert_f)), 200
    except FileNotFoundError as err:
        return jsonify(error=str(err)), 404
    except Exception:
        current_app.logger.exception("Dataset explorer failed")
        return jsonify(error="Could not load dataset explorer."), 500


@api_bp.get("/crop-stages")
def crop_stages():
    crop = request.args.get("crop", "").strip()
    return jsonify(get_crop_stages(crop)), 200


@api_bp.get("/iot/latest")
def iot_latest():
    query = (
        SensorReading.query.filter_by(user_id=current_user.id)
        if current_user.is_authenticated
        else SensorReading.query.filter(SensorReading.user_id.is_(None))
    )
    rows = query.order_by(SensorReading.recorded_at.desc(), SensorReading.id.desc()).limit(10).all()
    return jsonify({
        "latest": rows[0].to_dict() if rows else None,
        "history": [r.to_dict() for r in rows],
    }), 200


@api_bp.post("/iot/ingest")
def iot_ingest():
    if Config.IOT_DEVICE_TOKEN:
        token = request.headers.get("X-Device-Token", "").strip()
        if token != Config.IOT_DEVICE_TOKEN:
            return jsonify(error="Unauthorized IoT device token."), 401

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="Invalid sensor JSON payload."), 400

    try:
        validated = validate_soil_payload(data, require_crop=False)
    except ValueError as err:
        return jsonify(error=str(err)), 400

    device_id = str(data.get("device_id", "ESP32-NODE-01")).strip()[:64] or "ESP32-NODE-01"
    reading = SensorReading(
        user_id=current_user.id if current_user.is_authenticated else None,
        device_id=device_id,
        soil_type=validated["soil_type"],
        temperature=validated["temperature"],
        humidity=validated["humidity"],
        moisture=validated["moisture"],
        nitrogen=validated["nitrogen"],
        phosphorus=validated["phosphorus"],
        potassium=validated["potassium"],
        ph=validated["ph"],
        is_simulated=bool(data.get("is_simulated", False)),
        display_time=datetime.now().strftime("%d %b %Y, %I:%M:%S %p"),
        recorded_at=datetime.now(timezone.utc),
    )
    db.session.add(reading)
    db.session.commit()
    return jsonify({"reading": reading.to_dict(), "status": "ingested"}), 201


@api_bp.post("/iot/simulate")
def iot_simulate():
    data = request.get_json(silent=True) or {}
    soil_type = str(data.get("soil_type", "")).strip()
    if soil_type not in Config.ALLOWED_SOILS:
        soil_type = random.choice(Config.ALLOWED_SOILS)

    reading = SensorReading(
        user_id=current_user.id if current_user.is_authenticated else None,
        device_id="SIM-ESP32-DEMO",
        soil_type=soil_type,
        temperature=round(random.uniform(22.0, 35.5), 1),
        humidity=round(random.uniform(45.0, 82.0), 1),
        moisture=round(random.uniform(28.0, 72.0), 1),
        nitrogen=round(random.uniform(12.0, 95.0), 1),
        phosphorus=round(random.uniform(8.0, 65.0), 1),
        potassium=round(random.uniform(10.0, 75.0), 1),
        ph=round(random.uniform(5.2, 7.9), 1),
        is_simulated=True,
        display_time=datetime.now().strftime("%d %b %Y, %I:%M:%S %p"),
        recorded_at=datetime.now(timezone.utc),
    )
    db.session.add(reading)
    db.session.commit()
    return jsonify({"reading": reading.to_dict(), "status": "simulated"}), 201


@api_bp.post("/report/sample-tag")
def download_sample_tag_payload():
    data = request.get_json(silent=True) or {}
    try:
        buf = build_sample_bag_tag_pdf(
            report_uid=str(data.get("report_uid", "")),
            crop=str(data.get("crop", "Not specified")),
            soil_type=str(data.get("soil_type", "Not specified")),
            plot_name=str(data.get("plot_name", "")),
            collection_date=str(data.get("date", "")),
        )
        return send_file(
            buf,
            mimetype="application/pdf",
            as_attachment=True,
            download_name="Agri_Nova_Soil_Sample_Tag.pdf",
        )
    except Exception:
        current_app.logger.exception("Sample bag tag PDF failed")
        return jsonify(error="Could not generate sample tag PDF."), 500


@api_bp.get("/report/sample-tag/<int:report_id>")
def download_sample_tag_by_id(report_id: int):
    report = _scoped_reports_query().filter(SoilReport.id == report_id).first()
    if not report:
        return jsonify(error="Report not found."), 404
    try:
        buf = build_sample_bag_tag_pdf(
            report_uid=report.report_uid,
            crop=report.crop,
            soil_type=report.soil_type or "Not recorded",
            plot_name=report.plot_name or "",
            collection_date=report.display_date,
        )
        return send_file(
            buf,
            mimetype="application/pdf",
            as_attachment=True,
            download_name=f"Agri_Nova_Tag_{report.report_uid}.pdf",
        )
    except Exception:
        current_app.logger.exception("Historical sample tag PDF failed")
        return jsonify(error="Could not generate sample tag PDF."), 500


@api_bp.post("/pest/analyze")
def pest_analyze():
    file = request.files.get("image")
    if not file or not file.filename:
        return jsonify(error="Please capture a camera photo or select an image file."), 400

    ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in {"jpg", "jpeg", "png", "webp", "bmp"}:
        return jsonify(error="Supported image formats: JPG, PNG, WEBP, or BMP."), 400

    mode = str(request.form.get("mode", "auto_hybrid")).strip()
    crop = str(request.form.get("crop", "")).strip()

    try:
        raw_bytes = file.read(6 * 1024 * 1024 + 1)
        result = analyze_pest_image(raw_bytes, mode=mode, crop=crop)

        now_local = datetime.now()
        scan_uid = f"PS-{now_local.strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        display_date = now_local.strftime("%d %b %Y, %I:%M %p")
        primary = result["primary_prediction"]
        ipm = result["ipm_guidance"]

        scan = PestScan(
            scan_uid=scan_uid,
            user_id=current_user.id if current_user.is_authenticated else None,
            crop=result["crop_context"],
            scan_mode=result["mode"],
            predicted_label=primary["label"],
            confidence_pct=primary["confidence_pct"],
            category=ipm["category"],
            severity=ipm["severity"],
            model_used=primary["model_used"],
            display_date=display_date,
            created_at=datetime.now(timezone.utc),
        )
        db.session.add(scan)
        db.session.commit()

        result["scan_id"] = scan.id
        result["scan_uid"] = scan.scan_uid
        result["date"] = display_date
        return jsonify(result), 200
    except ValueError as err:
        return jsonify(error=str(err)), 400
    except FileNotFoundError as err:
        return jsonify(error=str(err)), 500
    except Exception:
        current_app.logger.exception("Local ONNX pest vision analysis failed")
        return jsonify(error="Could not analyze image with local vision model."), 500


@api_bp.get("/pest/scans")
def pest_scans():
    query = (
        PestScan.query.filter_by(user_id=current_user.id)
        if current_user.is_authenticated
        else PestScan.query.filter(PestScan.user_id.is_(None))
    )
    rows = query.order_by(PestScan.created_at.desc(), PestScan.id.desc()).limit(25).all()
    return jsonify({"scans": [r.to_dict() for r in rows]}), 200


@api_bp.delete("/pest/scans/<int:scan_id>")
def delete_pest_scan(scan_id: int):
    query = (
        PestScan.query.filter_by(user_id=current_user.id)
        if current_user.is_authenticated
        else PestScan.query.filter(PestScan.user_id.is_(None))
    )
    scan = query.filter(PestScan.id == scan_id).first()
    if not scan:
        return jsonify(error="Scan record not found."), 404
    db.session.delete(scan)
    db.session.commit()
    return jsonify({"deleted": True, "id": scan_id}), 200


@api_bp.get("/pest/guide")
def pest_guide():
    q = request.args.get("q", "").strip().lower()
    items = get_pest_reference_guide()
    if q:
        items = [
            item for item in items
            if q in item["category"].lower()
            or q in item["examples"].lower()
            or q in item["summary"].lower()
            or q in item["pesticide_class"].lower()
        ]
    return jsonify({"items": items, "count": len(items)}), 200


# ==========================================
# FARM TASKS & SCOUTING CHECKLIST
# ==========================================

def _scoped_tasks_query():
    if current_user.is_authenticated:
        return FarmTask.query.filter_by(user_id=current_user.id)
    return FarmTask.query.filter(FarmTask.user_id.is_(None))


@api_bp.get("/tasks")
def list_tasks():
    query = _scoped_tasks_query()
    plot_id = request.args.get("plot_id", "").strip()
    if plot_id and plot_id != "all":
        try:
            query = query.filter(FarmTask.plot_id == int(plot_id))
        except ValueError:
            pass
    status = request.args.get("status", "all").strip().lower()
    if status == "pending":
        query = query.filter(FarmTask.completed.is_(False))
    elif status == "done":
        query = query.filter(FarmTask.completed.is_(True))

    rows = query.order_by(FarmTask.completed.asc(), FarmTask.created_at.desc()).all()
    return jsonify({"tasks": [t.to_dict() for t in rows]}), 200


@api_bp.post("/tasks")
def create_task():
    data = request.get_json(silent=True) or {}
    title = str(data.get("title", "")).strip()
    category = str(data.get("category", "Scouting")).strip()[:48] or "Scouting"
    due_date = str(data.get("due_date", "")).strip()[:32]
    notes = str(data.get("notes", "")).strip()[:255]
    if not title or len(title) > 140:
        return jsonify(error="Task title is required (max 140 characters)."), 400

    try:
        plot = _resolve_plot(data.get("plot_id"))
    except ValueError as err:
        return jsonify(error=str(err)), 400

    task = FarmTask(
        user_id=current_user.id if current_user.is_authenticated else None,
        plot_id=plot.id if plot else None,
        plot_name=plot.name if plot else None,
        title=title,
        category=category,
        due_date=due_date,
        notes=notes,
        completed=False,
    )
    db.session.add(task)
    db.session.commit()
    return jsonify({"task": task.to_dict()}), 201


@api_bp.patch("/tasks/<int:task_id>")
def toggle_task(task_id: int):
    task = _scoped_tasks_query().filter(FarmTask.id == task_id).first()
    if not task:
        return jsonify(error="Task not found."), 404
    data = request.get_json(silent=True) or {}
    if "completed" in data:
        task.completed = bool(data["completed"])
    else:
        task.completed = not task.completed
    db.session.commit()
    return jsonify({"task": task.to_dict()}), 200


@api_bp.delete("/tasks/<int:task_id>")
def delete_task(task_id: int):
    task = _scoped_tasks_query().filter(FarmTask.id == task_id).first()
    if not task:
        return jsonify(error="Task not found."), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({"deleted": True, "id": task_id}), 200


# ==========================================
# ONE-CLICK FARM AUDIT ZIP EXPORT
# ==========================================

@api_bp.get("/export/audit-zip")
def export_audit_zip():
    reports = _scoped_reports_query().order_by(SoilReport.created_at.desc(), SoilReport.id.desc()).all()
    plots = _scoped_plots_query().order_by(Plot.created_at.desc()).all()
    tasks = _scoped_tasks_query().order_by(FarmTask.created_at.desc()).all()
    scans_q = (
        PestScan.query.filter_by(user_id=current_user.id)
        if current_user.is_authenticated
        else PestScan.query.filter(PestScan.user_id.is_(None))
    )
    scans = scans_q.order_by(PestScan.created_at.desc()).all()

    zip_buf = BytesIO()
    with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
        # 1. Soil Reports CSV
        s_io = StringIO()
        sw = csv.writer(s_io)
        sw.writerow(["Report ID", "Date", "Plot", "Crop", "Soil Type", "Fertilizer", "Match Index", "N", "P", "K", "pH", "Moisture"])
        for r in reports:
            sw.writerow([
                _csv_safe(r.report_uid), _csv_safe(r.display_date), _csv_safe(r.plot_name or ""),
                _csv_safe(r.crop), _csv_safe(r.soil_type), _csv_safe(r.fertilizer),
                _csv_safe(r.score), _csv_safe(r.nitrogen), _csv_safe(r.phosphorus),
                _csv_safe(r.potassium), _csv_safe(r.ph), _csv_safe(r.moisture),
            ])
        zf.writestr("soil_reports.csv", s_io.getvalue())

        # 2. Pest & Camera Scans CSV
        p_io = StringIO()
        pw = csv.writer(p_io)
        pw.writerow(["Scan ID", "Date", "Crop", "Mode", "Predicted Label", "Confidence %", "Category", "Severity", "Model"])
        for s in scans:
            pw.writerow([
                _csv_safe(s.scan_uid), _csv_safe(s.display_date), _csv_safe(s.crop),
                _csv_safe(s.scan_mode), _csv_safe(s.predicted_label), _csv_safe(s.confidence_pct),
                _csv_safe(s.category), _csv_safe(s.severity), _csv_safe(s.model_used),
            ])
        zf.writestr("pest_camera_scans.csv", p_io.getvalue())

        # 3. Plots & Tasks JSON
        zf.writestr("field_plots.json", json.dumps([p.to_dict() for p in plots], indent=2))
        zf.writestr("farm_tasks.json", json.dumps([t.to_dict() for t in tasks], indent=2))

        # 4. Latest Soil Report PDF (if available)
        if reports:
            latest = reports[0].to_dict(include_details=True)
            inputs = {
                "crop": latest["crop"], "soil_type": latest["soil_type"],
                "plot_name": latest.get("plot_name", ""), "temperature": latest["temperature"],
                "humidity": latest["humidity"], "moisture": latest["moisture"],
                "nitrogen": latest["nitrogen"], "phosphorus": latest["phosphorus"],
                "potassium": latest["potassium"], "ph": latest["ph"],
            }
            pdf_buf = build_soil_report_pdf(inputs=inputs, result=latest, report_uid=latest["report_uid"])
            zf.writestr(f"latest_soil_report_{latest['report_uid']}.pdf", pdf_buf.getvalue())

        # 5. Audit README
        zf.writestr(
            "README_AUDIT.txt",
            (
                "AGRI NOVA AI - FARM AUDIT BUNDLE\n"
                "=================================\n"
                f"Exported: {datetime.now().strftime('%d %B %Y, %I:%M %p')}\n"
                f"Soil Reports: {len(reports)}\n"
                f"Pest Camera Scans: {len(scans)}\n"
                f"Field Plots: {len(plots)}\n"
                f"Farm Tasks: {len(tasks)}\n\n"
                "Disclaimer: Academic prototype outputs only. Verify agronomic decisions with a certified soil lab or agronomist.\n"
            ),
        )

    zip_buf.seek(0)
    return send_file(
        zip_buf,
        mimetype="application/zip",
        as_attachment=True,
        download_name="Agri_Nova_AI_Farm_Audit.zip",
    )
