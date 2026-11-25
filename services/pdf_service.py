from datetime import datetime
from io import BytesIO
import json
from xml.sax.saxutils import escape

import qrcode
from reportlab.graphics.charts.barcharts import HorizontalBarChart
from reportlab.graphics.shapes import Drawing, String
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    Image as RLImage,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

PRIMARY_GREEN = colors.HexColor("#247A49")
DARK_GREEN = colors.HexColor("#123B26")
LIGHT_GREEN = colors.HexColor("#E6F2E9")
SOFT_BG = colors.HexColor("#F5F8F5")
BORDER_GREEN = colors.HexColor("#D2E2D5")
TEXT_DARK = colors.HexColor("#26352B")
TEXT_MUTED = colors.HexColor("#5B6E61")


class NumberedCanvas(canvas.Canvas):
    """Canvas subclass that renders page numbers ('Page X of Y') cleanly in the footer."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self._draw_footer(total_pages)
            super().showPage()
        super().save()

    def _draw_footer(self, page_count: int):
        self.saveState()
        self.setStrokeColor(BORDER_GREEN)
        self.setLineWidth(0.6)
        self.line(18 * mm, 15 * mm, A4[0] - 18 * mm, 15 * mm)
        self.setFont("Helvetica", 8)
        self.setFillColor(TEXT_MUTED)
        self.drawString(
            18 * mm,
            10.5 * mm,
            "Agri Nova AI | Precision Agriculture Academic Prototype",
        )
        self.drawRightString(
            A4[0] - 18 * mm,
            10.5 * mm,
            f"Page {self._pageNumber} of {page_count}",
        )
        self.restoreState()


def _safe(value) -> str:
    return escape(str(value if value is not None and value != "" else "Not recorded"))


def _build_qr_image(payload_dict: dict) -> RLImage | None:
    """Generate a compact QR verification stamp as an in-memory PNG for ReportLab."""
    try:
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=4,
            border=2,
        )
        qr.add_data(json.dumps(payload_dict, separators=(",", ":")))
        qr.make(fit=True)
        img = qr.make_image(fill_color="#123B26", back_color="#FFFFFF")
        img_buf = BytesIO()
        img.save(img_buf, format="PNG")
        img_buf.seek(0)
        return RLImage(img_buf, width=22 * mm, height=22 * mm)
    except Exception:
        return None


def _build_npk_chart(gaps: list[dict]) -> Drawing | None:
    """Create a compact ReportLab horizontal bar chart for NPK prototype percentages."""
    if not gaps:
        return None
    labels = [str(g.get("name", "")) for g in gaps]
    values = [max(0, min(100, float(g.get("percent", 0) or 0))) for g in gaps]

    drawing = Drawing(470, 115)
    drawing.add(
        String(
            0,
            102,
            "NPK Prototype Target Match (% of illustrative crop baseline)",
            fontName="Helvetica-Bold",
            fontSize=9,
            fillColor=DARK_GREEN,
        )
    )
    chart = HorizontalBarChart()
    chart.x = 85
    chart.y = 12
    chart.height = 80
    chart.width = 365
    chart.data = [values]
    chart.categoryAxis.categoryNames = labels
    chart.categoryAxis.labels.fontName = "Helvetica-Bold"
    chart.categoryAxis.labels.fontSize = 8.5
    chart.categoryAxis.labels.fillColor = TEXT_DARK
    chart.valueAxis.valueMin = 0
    chart.valueAxis.valueMax = 100
    chart.valueAxis.valueStep = 25
    chart.valueAxis.labels.fontSize = 8
    chart.valueAxis.labels.fillColor = TEXT_MUTED
    chart.valueAxis.gridStrokeColor = BORDER_GREEN
    chart.valueAxis.visibleGrid = True
    chart.bars[0].fillColor = PRIMARY_GREEN
    chart.bars[0].strokeColor = DARK_GREEN
    chart.barLabelFormat = "%d%%"
    chart.barLabels.nudge = 8
    chart.barLabels.fontSize = 8
    chart.barLabels.fillColor = DARK_GREEN
    drawing.add(chart)
    return drawing


def build_soil_report_pdf(inputs: dict, result: dict, report_uid: str = "") -> BytesIO:
    """Build a polished, compact A4 PDF soil analysis report with QR verification stamp."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=22 * mm,
        title="Agri Nova AI Soil Analysis Report",
    )

    styles = getSampleStyleSheet()
    heading_style = ParagraphStyle(
        "AgriHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        textColor=DARK_GREEN,
        spaceBefore=10,
        spaceAfter=5,
    )
    body_style = ParagraphStyle(
        "AgriBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.5,
        textColor=TEXT_DARK,
    )
    small_muted = ParagraphStyle(
        "AgriSmallMuted",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=TEXT_MUTED,
    )

    generated_ts = result.get("date") or datetime.now().strftime("%d %B %Y, %I:%M %p")
    uid_text = report_uid or result.get("report_uid") or f"AN-{datetime.now().strftime('%Y%m%d-%H%M')}"
    score_val = result.get("score", "N/A")
    fert_val = result.get("fertilizer", "N/A")
    crop_val = inputs.get("crop") or result.get("crop") or "N/A"
    soil_val = inputs.get("soil_type") or result.get("soil_type") or "Not recorded"
    plot_val = result.get("plot_name") or inputs.get("plot_name") or ""

    qr_img = _build_qr_image({
        "app": "Agri Nova AI",
        "id": uid_text,
        "crop": crop_val,
        "soil": soil_val,
        "fert": fert_val,
        "score": score_val,
        "date": generated_ts,
        "prototype": True,
    })

    story = []

    # Branded header banner with embedded QR verification stamp
    right_cell = [
        Paragraph(
            f"<font color='#E6F2E9' size='8.5'><b>Report ID:</b> {_safe(uid_text)}<br/>"
            f"<b>Generated:</b> {_safe(generated_ts)}"
            + (f"<br/><b>Plot:</b> {_safe(plot_val)}" if plot_val else "")
            + "</font>",
            ParagraphStyle("BannerRight", parent=body_style, alignment=2),
        )
    ]
    if qr_img is not None:
        banner_table = Table(
            [[
                Paragraph(
                    "<font color='#FFFFFF' size='16'><b>AGRI NOVA AI</b></font><br/>"
                    "<font color='#E6F2E9' size='9'>Precision Agriculture. Smarter Decisions. Sustainable Farming.</font>",
                    body_style,
                ),
                right_cell[0],
                qr_img,
            ]],
            colWidths=[245, 175, 70],
        )
    else:
        banner_table = Table(
            [[
                Paragraph(
                    "<font color='#FFFFFF' size='16'><b>AGRI NOVA AI</b></font><br/>"
                    "<font color='#E6F2E9' size='9'>Precision Agriculture. Smarter Decisions. Sustainable Farming.</font>",
                    body_style,
                ),
                right_cell[0],
            ]],
            colWidths=[295, 195],
        )

    banner_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DARK_GREEN),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (-1, 0), (-1, 0), "RIGHT"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    story.append(banner_table)
    story.append(Spacer(1, 9))

    # Executive Summary Strip
    summary_cards = Table(
        [[
            Paragraph(f"<font size='8' color='#5B6E61'>SELECTED CROP</font><br/><b><font size='11' color='#123B26'>{_safe(crop_val)}</font></b>", body_style),
            Paragraph(f"<font size='8' color='#5B6E61'>SOIL TYPE</font><br/><b><font size='11' color='#123B26'>{_safe(soil_val)}</font></b>", body_style),
            Paragraph(f"<font size='8' color='#5B6E61'>DEMO MATCH INDEX</font><br/><b><font size='11' color='#247A49'>{_safe(score_val)} / 100</font></b>", body_style),
            Paragraph(f"<font size='8' color='#5B6E61'>ML PREDICTION</font><br/><b><font size='11' color='#247A49'>{_safe(fert_val)}</font></b>", body_style),
        ]],
        colWidths=[115, 115, 125, 135],
    )
    summary_cards.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GREEN),
        ("BOX", (0, 0), (-1, -1), 0.75, BORDER_GREEN),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER_GREEN),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    story.append(summary_cards)

    # 1. Soil Profile Table
    story.append(Paragraph("1. Soil Profile & Environmental Inputs", heading_style))
    soil_rows = [
        ["Parameter", "Recorded Value", "Parameter", "Recorded Value"],
        ["Crop Type", _safe(crop_val), "Soil Type", _safe(soil_val)],
        ["Nitrogen (N)", f"{_safe(inputs.get('nitrogen'))} kg/ha*", "Temperature", f"{_safe(inputs.get('temperature'))} °C"],
        ["Phosphorus (P)", f"{_safe(inputs.get('phosphorus'))} kg/ha*", "Humidity", f"{_safe(inputs.get('humidity'))} %"],
        ["Potassium (K)", f"{_safe(inputs.get('potassium'))} kg/ha*", "Soil Moisture", f"{_safe(inputs.get('moisture'))} %"],
        ["Soil pH", _safe(inputs.get("ph")), "Model Type", "Random Forest (Prototype)"],
    ]
    soil_table = Table(soil_rows, colWidths=[110, 135, 110, 135], repeatRows=1)
    soil_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY_GREEN),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, SOFT_BG]),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_GREEN),
        ("PADDING", (0, 0), (-1, -1), 5.5),
        ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (2, 1), (2, -1), "Helvetica-Bold"),
        ("TEXTCOLOR", (0, 1), (-1, -1), TEXT_DARK),
    ]))
    story.append(soil_table)
    story.append(Spacer(1, 3))
    story.append(Paragraph("*NPK units are illustrative; match units from your certified soil lab report.", small_muted))

    # 2. NPK Observations & Visual Chart
    gaps = result.get("gaps") or []
    if gaps:
        story.append(Paragraph("2. NPK Prototype Observations", heading_style))
        nutrient_data = [["Nutrient", "Status", "Prototype Baseline Match"]]
        for item in gaps:
            nutrient_data.append([
                _safe(item.get("name", "")),
                _safe(item.get("status", "")),
                f"{_safe(item.get('percent', '0'))}%",
            ])
        nutrient_table = Table(nutrient_data, colWidths=[165, 175, 150], repeatRows=1)
        nutrient_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), PRIMARY_GREEN),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, SOFT_BG]),
            ("GRID", (0, 0), (-1, -1), 0.5, BORDER_GREEN),
            ("PADDING", (0, 0), (-1, -1), 5.5),
        ]))
        story.append(nutrient_table)
        story.append(Spacer(1, 5))

        chart = _build_npk_chart(gaps)
        if chart is not None:
            story.append(chart)

    # 3. Crop Health Insights
    health = result.get("health") or {}
    if health:
        story.append(Paragraph("3. Crop Health Insights", heading_style))
        story.append(
            Paragraph(
                f"<b>Overall Status:</b> {_safe(health.get('overall', 'N/A'))} — {_safe(health.get('note', ''))}",
                body_style,
            )
        )
        story.append(Spacer(1, 4))
        for obs in health.get("observations", []):
            story.append(
                Paragraph(
                    f"<b>{_safe(obs.get('title', ''))}</b> [{_safe(obs.get('status', ''))}]: {_safe(obs.get('detail', ''))}",
                    body_style,
                )
            )
            story.append(Spacer(1, 2))

    # 4. Recommended Checks
    actions = result.get("actions") or []
    if actions:
        story.append(Paragraph("4. Recommended Verification Checks", heading_style))
        for action in actions:
            story.append(Paragraph(f"• {_safe(action)}", body_style))
            story.append(Spacer(1, 2))

    disclaimer_text = result.get("disclaimer") or (
        "Academic ML prototype trained on a small 99-record dataset. Predictions are not "
        "validated agricultural prescriptions. Confirm fertilizer choice and rates with a "
        "certified soil laboratory or agronomist."
    )
    story.append(Spacer(1, 8))
    disc_table = Table(
        [[
            Paragraph(
                f"<b>Important Academic Prototype Disclaimer:</b> {_safe(disclaimer_text)} "
                f"(Scan the header QR stamp to verify Report ID {_safe(uid_text)}.)",
                ParagraphStyle("DiscStyle", parent=small_muted, textColor=colors.HexColor("#6D511C")),
            )
        ]],
        colWidths=[490],
    )
    disc_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF8E8")),
        ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#E7D099")),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(disc_table)

    doc.build(story, canvasmaker=NumberedCanvas)
    buffer.seek(0)
    return buffer


def build_sample_bag_tag_pdf(
    report_uid: str = "",
    crop: str = "Not specified",
    soil_type: str = "Not specified",
    plot_name: str = "",
    collection_date: str = "",
) -> BytesIO:
    """Build a compact printable A6 Soil Sample Bag Tag PDF with a QR code for lab submission."""
    buffer = BytesIO()
    page_w, page_h = 105 * mm, 148 * mm
    doc = SimpleDocTemplate(
        buffer,
        pagesize=(page_w, page_h),
        rightMargin=8 * mm,
        leftMargin=8 * mm,
        topMargin=8 * mm,
        bottomMargin=8 * mm,
        title="Agri Nova AI Soil Sample Tag",
    )

    styles = getSampleStyleSheet()
    body_style = ParagraphStyle(
        "TagBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=TEXT_DARK,
    )

    uid_text = report_uid or f"TAG-{datetime.now().strftime('%Y%m%d-%H%M')}"
    date_text = collection_date or datetime.now().strftime("%d %b %Y, %I:%M %p")

    qr_img = _build_qr_image({
        "tag_type": "Soil Lab Sample Bag",
        "id": uid_text,
        "plot": plot_name or "General",
        "crop": crop,
        "soil": soil_type,
        "date": date_text,
    })

    story = []
    header_tbl = Table(
        [[Paragraph(
            "<font color='#FFFFFF' size='11'><b>AGRI NOVA AI</b></font><br/>"
            "<font color='#E6F2E9' size='7.5'>SOIL LAB SAMPLE COLLECTION TAG</font>",
            body_style,
        )]],
        colWidths=[89 * mm],
    )
    header_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DARK_GREEN),
        ("PADDING", (0, 0), (-1, -1), 7),
    ]))
    story.append(header_tbl)
    story.append(Spacer(1, 6))

    meta_rows = [
        ["Sample / Report ID", _safe(uid_text)],
        ["Collection Date", _safe(date_text)],
        ["Field / Plot", _safe(plot_name or "General Workspace")],
        ["Intended Crop", _safe(crop)],
        ["Observed Soil Type", _safe(soil_type)],
        ["Requested Lab Tests", "[ ] NPK   [ ] pH   [ ] EC   [ ] OC"],
        ["Sample Depth", "0–15 cm (Composite)"],
    ]
    meta_tbl = Table(meta_rows, colWidths=[34 * mm, 55 * mm])
    meta_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), LIGHT_GREEN),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7.8),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_GREEN),
        ("PADDING", (0, 0), (-1, -1), 4.5),
        ("TEXTCOLOR", (0, 0), (-1, -1), TEXT_DARK),
    ]))
    story.append(meta_tbl)
    story.append(Spacer(1, 7))

    if qr_img is not None:
        qr_row = Table(
            [[
                qr_img,
                Paragraph(
                    f"<b>Scan Tag QR</b><br/>ID: {_safe(uid_text)}<br/>"
                    "Attach securely to sample bag before submitting to a certified soil testing laboratory.",
                    ParagraphStyle("QrNote", parent=body_style, fontSize=7.5, leading=10.5, textColor=TEXT_MUTED),
                ),
            ]],
            colWidths=[26 * mm, 63 * mm],
        )
        qr_row.setStyle(TableStyle([
            ("BOX", (0, 0), (-1, -1), 0.5, BORDER_GREEN),
            ("BACKGROUND", (0, 0), (-1, -1), SOFT_BG),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("PADDING", (0, 0), (-1, -1), 5),
        ]))
        story.append(qr_row)

    doc.build(story)
    buffer.seek(0)
    return buffer


def build_comparison_pdf(reports: list[dict]) -> BytesIO:
    """Build a multi-report side-by-side comparison A4 PDF."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=16 * mm,
        leftMargin=16 * mm,
        topMargin=16 * mm,
        bottomMargin=22 * mm,
        title="Agri Nova AI Multi-Report Comparison",
    )
    styles = getSampleStyleSheet()
    body_style = ParagraphStyle(
        "CmpBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12.5,
        textColor=TEXT_DARK,
    )

    story = [
        Table(
            [[
                Paragraph(
                    "<font color='#FFFFFF' size='15'><b>AGRI NOVA AI — COMPARISON REPORT</b></font><br/>"
                    "<font color='#E6F2E9' size='8.5'>Side-by-Side Soil &amp; ML Prediction Comparison</font>",
                    body_style,
                ),
                Paragraph(
                    f"<font color='#E6F2E9' size='8.5'><b>Generated:</b> {datetime.now().strftime('%d %b %Y, %I:%M %p')}<br/>"
                    f"<b>Reports Compared:</b> {len(reports)}</font>",
                    ParagraphStyle("CmpRight", parent=body_style, alignment=2),
                ),
            ]],
            colWidths=[305, 195],
            style=TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), DARK_GREEN),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("PADDING", (0, 0), (-1, -1), 10),
            ]),
        ),
        Spacer(1, 12),
    ]

    headers = ["Metric"] + [f"{r.get('report_uid', '')}\n({r.get('crop', '')})" for r in reports]
    rows = [headers]
    metrics = [
        ("Date", lambda r: r.get("date") or "—"),
        ("Field Plot", lambda r: r.get("plot_name") or "—"),
        ("Crop", lambda r: r.get("crop") or "—"),
        ("Soil Type", lambda r: r.get("soil_type") or "Not recorded"),
        ("ML Fertilizer", lambda r: r.get("fertilizer") or "Not recorded"),
        ("Demo Match Index", lambda r: f"{r.get('score', '--')}/100"),
        ("Nitrogen (kg/ha*)", lambda r: r.get("nitrogen") if r.get("nitrogen") is not None else "N/A"),
        ("Phosphorus (kg/ha*)", lambda r: r.get("phosphorus") if r.get("phosphorus") is not None else "N/A"),
        ("Potassium (kg/ha*)", lambda r: r.get("potassium") if r.get("potassium") is not None else "N/A"),
        ("Soil pH", lambda r: r.get("ph") if r.get("ph") is not None else "N/A"),
        ("Moisture (%)", lambda r: f"{r.get('moisture')}%" if r.get("moisture") is not None else "N/A"),
        ("Temperature (°C)", lambda r: r.get("temperature") if r.get("temperature") is not None else "N/A"),
    ]
    for label, fn in metrics:
        rows.append([label] + [_safe(fn(r)) for r in reports])

    first_w = 125
    col_w = (500 - first_w) / max(1, len(reports))
    tbl = Table(rows, colWidths=[first_w] + [col_w] * len(reports), repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY_GREEN),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, SOFT_BG]),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_GREEN),
        ("PADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 12))
    story.append(
        Table(
            [[Paragraph(
                "<b>Academic Prototype Notice:</b> ML predictions come from a 99-record educational Random Forest dataset "
                "and Match Indices use illustrative baselines. Confirm agronomic decisions with a certified soil lab.",
                ParagraphStyle("CmpDisc", parent=body_style, fontSize=8, textColor=colors.HexColor("#6D511C")),
            )]],
            colWidths=[500],
            style=TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF8E8")),
                ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#E7D099")),
                ("PADDING", (0, 0), (-1, -1), 8),
            ]),
        )
    )

    doc.build(story, canvasmaker=NumberedCanvas)
    buffer.seek(0)
    return buffer
