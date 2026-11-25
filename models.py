import json
from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    full_name = db.Column(db.String(120), nullable=False, default="")
    farm_location = db.Column(db.String(120), nullable=False, default="")
    password_hash = db.Column(db.String(256), nullable=False)
    preferred_theme = db.Column(db.String(24), nullable=False, default="light")
    preferred_units = db.Column(db.String(24), nullable=False, default="metric")
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    reports = db.relationship(
        "SoilReport",
        back_populates="user",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )
    plots = db.relationship(
        "Plot",
        back_populates="user",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name or self.username,
            "farm_location": self.farm_location,
            "preferred_theme": self.preferred_theme,
            "preferred_units": self.preferred_units,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Plot(db.Model):
    __tablename__ = "plots"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    name = db.Column(db.String(80), nullable=False)
    soil_type = db.Column(db.String(32), nullable=False, default="Loamy")
    location = db.Column(db.String(120), nullable=False, default="")
    area_acres = db.Column(db.Float, nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    notes = db.Column(db.String(255), nullable=False, default="")
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    user = db.relationship("User", back_populates="plots")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "soil_type": self.soil_type,
            "location": self.location,
            "area_acres": self.area_acres,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class SoilReport(db.Model):
    __tablename__ = "soil_reports"

    id = db.Column(db.Integer, primary_key=True)
    report_uid = db.Column(db.String(32), unique=True, nullable=False, index=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    plot_id = db.Column(
        db.Integer,
        db.ForeignKey("plots.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    plot_name = db.Column(db.String(80), nullable=True)

    crop = db.Column(db.String(64), nullable=False, index=True)
    soil_type = db.Column(db.String(32), nullable=True)
    temperature = db.Column(db.Float, nullable=True)
    humidity = db.Column(db.Float, nullable=True)
    moisture = db.Column(db.Float, nullable=True)
    nitrogen = db.Column(db.Float, nullable=True)
    phosphorus = db.Column(db.Float, nullable=True)
    potassium = db.Column(db.Float, nullable=True)
    ph = db.Column(db.Float, nullable=True)

    score = db.Column(db.Integer, nullable=False)
    fertilizer = db.Column(db.String(64), nullable=False, default="Not recorded")
    summary = db.Column(db.String(255), nullable=False, default="")

    gaps_json = db.Column(db.Text, nullable=False, default="[]")
    health_json = db.Column(db.Text, nullable=False, default="{}")
    actions_json = db.Column(db.Text, nullable=False, default="[]")
    probs_json = db.Column(db.Text, nullable=False, default="[]")
    disclaimer = db.Column(db.Text, nullable=False, default="")

    source = db.Column(db.String(32), nullable=False, default="analysis")
    display_date = db.Column(db.String(64), nullable=False, default="")
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )

    user = db.relationship("User", back_populates="reports")

    def to_dict(self, include_details: bool = True) -> dict:
        data = {
            "id": self.id,
            "report_uid": self.report_uid,
            "user_id": self.user_id,
            "plot_id": self.plot_id,
            "plot_name": self.plot_name or "",
            "crop": self.crop,
            "soil_type": self.soil_type or "Not recorded",
            "temperature": self.temperature,
            "humidity": self.humidity,
            "moisture": self.moisture,
            "nitrogen": self.nitrogen,
            "phosphorus": self.phosphorus,
            "potassium": self.potassium,
            "ph": self.ph,
            "score": self.score,
            "fertilizer": self.fertilizer or "Not recorded",
            "summary": self.summary,
            "source": self.source,
            "date": self.display_date,
            "created": self.display_date,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
        if include_details:
            for attr, key, fallback in [
                ("gaps_json", "gaps", []),
                ("health_json", "health", {}),
                ("actions_json", "actions", []),
                ("probs_json", "tree_vote_distribution", []),
            ]:
                try:
                    data[key] = json.loads(getattr(self, attr) or json.dumps(fallback))
                except ValueError:
                    data[key] = fallback
            data["disclaimer"] = self.disclaimer
        return data


class SensorReading(db.Model):
    __tablename__ = "sensor_readings"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    device_id = db.Column(db.String(64), nullable=False, default="ESP32-NODE-01")
    soil_type = db.Column(db.String(32), nullable=False, default="Loamy")
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    moisture = db.Column(db.Float, nullable=False)
    nitrogen = db.Column(db.Float, nullable=False)
    phosphorus = db.Column(db.Float, nullable=False)
    potassium = db.Column(db.Float, nullable=False)
    ph = db.Column(db.Float, nullable=False)
    is_simulated = db.Column(db.Boolean, nullable=False, default=False)
    display_time = db.Column(db.String(64), nullable=False, default="")
    recorded_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "device_id": self.device_id,
            "soil_type": self.soil_type,
            "temperature": self.temperature,
            "humidity": self.humidity,
            "moisture": self.moisture,
            "nitrogen": self.nitrogen,
            "phosphorus": self.phosphorus,
            "potassium": self.potassium,
            "ph": self.ph,
            "is_simulated": self.is_simulated,
            "display_time": self.display_time,
            "recorded_at": self.recorded_at.isoformat() if self.recorded_at else None,
        }


class PestScan(db.Model):
    __tablename__ = "pest_scans"

    id = db.Column(db.Integer, primary_key=True)
    scan_uid = db.Column(db.String(32), unique=True, nullable=False, index=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    crop = db.Column(db.String(64), nullable=False, default="Not specified")
    scan_mode = db.Column(db.String(32), nullable=False, default="auto_hybrid")
    predicted_label = db.Column(db.String(120), nullable=False)
    confidence_pct = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(80), nullable=False)
    severity = db.Column(db.String(48), nullable=False)
    model_used = db.Column(db.String(96), nullable=False)
    display_date = db.Column(db.String(64), nullable=False, default="")
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "scan_uid": self.scan_uid,
            "crop": self.crop,
            "scan_mode": self.scan_mode,
            "predicted_label": self.predicted_label,
            "confidence_pct": self.confidence_pct,
            "category": self.category,
            "severity": self.severity,
            "model_used": self.model_used,
            "date": self.display_date,
        }


class FarmTask(db.Model):
    __tablename__ = "farm_tasks"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    plot_id = db.Column(
        db.Integer,
        db.ForeignKey("plots.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    plot_name = db.Column(db.String(80), nullable=True)
    title = db.Column(db.String(140), nullable=False)
    category = db.Column(db.String(48), nullable=False, default="Scouting")
    due_date = db.Column(db.String(32), nullable=False, default="")
    notes = db.Column(db.String(255), nullable=False, default="")
    completed = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "plot_id": self.plot_id,
            "plot_name": self.plot_name or "",
            "title": self.title,
            "category": self.category,
            "due_date": self.due_date,
            "notes": self.notes,
            "completed": self.completed,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
