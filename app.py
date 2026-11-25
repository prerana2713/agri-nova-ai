import json
import logging
import os
from datetime import datetime, timedelta, timezone

from flask import Flask, jsonify, render_template
from sqlalchemy import text

from config import Config
from extensions import db, login_manager
from models import FarmTask, PestScan, Plot, SensorReading, SoilReport, User  # noqa: F401
from routes.api import api_bp
from routes.auth import auth_bp
from services.ml_service import get_model


def _configure_logging(app: Flask) -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    app.logger.setLevel(logging.INFO)


def _ensure_sqlite_columns(app: Flask) -> None:
    """Safely add newly introduced SoilReport columns if upgrading an existing agri_nova.db."""
    try:
        rows = db.session.execute(text("PRAGMA table_info(soil_reports)")).fetchall()
        existing = {row[1] for row in rows}
        additions = [
            ("plot_id", "INTEGER"),
            ("plot_name", "VARCHAR(80)"),
            ("probs_json", "TEXT NOT NULL DEFAULT '[]'"),
        ]
        for col_name, col_def in additions:
            if col_name not in existing:
                db.session.execute(
                    text(f"ALTER TABLE soil_reports ADD COLUMN {col_name} {col_def}")
                )
                app.logger.info("Added column %s to soil_reports.", col_name)

        plot_rows = db.session.execute(text("PRAGMA table_info(plots)")).fetchall()
        plot_existing = {row[1] for row in plot_rows}
        for col_name, col_def in [("latitude", "FLOAT"), ("longitude", "FLOAT")]:
            if col_name not in plot_existing:
                db.session.execute(
                    text(f"ALTER TABLE plots ADD COLUMN {col_name} {col_def}")
                )
                app.logger.info("Added column %s to plots.", col_name)

        db.session.commit()
    except Exception:
        db.session.rollback()
        app.logger.exception("SQLite schema check failed")


def _migrate_legacy_history(app: Flask) -> None:
    """Import existing history.json records into SQLite once without deleting history.json."""
    if SoilReport.query.first() is not None:
        return

    path = Config.LEGACY_HISTORY_PATH
    if not os.path.exists(path):
        return

    try:
        with open(path, "r", encoding="utf-8") as fh:
            records = json.load(fh)
    except (OSError, ValueError):
        app.logger.warning("Could not parse legacy history.json during migration.")
        return

    if not isinstance(records, list) or not records:
        return

    base_time = datetime.now(timezone.utc)
    imported = 0
    for idx, item in enumerate(records):
        if not isinstance(item, dict):
            continue
        crop = str(item.get("crop") or "Unknown").strip()
        display_date = str(item.get("date") or item.get("created") or "").strip()
        try:
            parsed_dt = datetime.strptime(display_date, "%d %b %Y, %I:%M %p").replace(
                tzinfo=timezone.utc
            )
        except ValueError:
            parsed_dt = base_time - timedelta(minutes=idx + 1)

        report = SoilReport(
            report_uid=str(item.get("report_uid") or f"AN-LEGACY-{idx + 1:04d}"),
            user_id=None,
            crop=crop,
            soil_type=item.get("soil_type") or "Not recorded",
            score=int(item.get("score") or 0),
            fertilizer=str(item.get("fertilizer") or "Not recorded"),
            summary=str(item.get("summary") or "Imported legacy soil analysis"),
            disclaimer=Config.PROTOTYPE_DISCLAIMER,
            source="legacy_json",
            display_date=display_date or parsed_dt.strftime("%d %b %Y, %I:%M %p"),
            created_at=parsed_dt,
        )
        db.session.add(report)
        imported += 1

    if imported:
        db.session.commit()
        app.logger.info("Migrated %d legacy records from history.json to SQLite.", imported)


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    _configure_logging(app)

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id: str):
        try:
            return db.session.get(User, int(user_id))
        except (TypeError, ValueError):
            return None

    @login_manager.unauthorized_handler
    def unauthorized():
        return jsonify(error="Authentication required."), 401

    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)

    @app.get("/")
    def home():
        return render_template(
            "index.html",
            crops=list(Config.CROP_MAPPING.keys()),
            soils=Config.ALLOWED_SOILS,
        )

    @app.errorhandler(404)
    def handle_404(_err):
        return jsonify(error="Requested resource was not found."), 404

    @app.errorhandler(500)
    def handle_500(_err):
        return jsonify(error="Internal server error."), 500

    with app.app_context():
        db.create_all()
        _ensure_sqlite_columns(app)
        _migrate_legacy_history(app)
        try:
            get_model()
            app.logger.info("Random Forest model loaded successfully.")
        except Exception:
            app.logger.exception("Failed to preload Random Forest model.")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
