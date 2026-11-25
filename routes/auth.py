import re
from flask import Blueprint, jsonify, request
from flask_login import current_user, login_user, logout_user

from extensions import db
from models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_USERNAME_RE = re.compile(r"^[A-Za-z0-9_.-]{3,32}$")


@auth_bp.get("/me")
def get_me():
    if not current_user.is_authenticated:
        return jsonify({"authenticated": False, "user": None}), 200
    return jsonify({"authenticated": True, "user": current_user.to_dict()}), 200


@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    username = str(data.get("username", "")).strip()
    email = str(data.get("email", "")).strip().lower()
    full_name = str(data.get("full_name", "")).strip()
    farm_location = str(data.get("farm_location", "")).strip()
    password = str(data.get("password", ""))

    if not _USERNAME_RE.match(username):
        return jsonify(
            error="Username must be 3–32 characters (letters, numbers, _, ., -)."
        ), 400
    if not _EMAIL_RE.match(email):
        return jsonify(error="Please provide a valid email address."), 400
    if len(password) < 6:
        return jsonify(error="Password must be at least 6 characters."), 400

    if User.query.filter_by(username=username).first():
        return jsonify(error="That username is already taken."), 409
    if User.query.filter_by(email=email).first():
        return jsonify(error="An account with that email already exists."), 409

    user = User(
        username=username,
        email=email,
        full_name=full_name[:120] or username,
        farm_location=farm_location[:120],
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    login_user(user, remember=True)
    return jsonify({"authenticated": True, "user": user.to_dict()}), 201


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    identifier = str(data.get("identifier", "")).strip()
    password = str(data.get("password", ""))

    if not identifier or not password:
        return jsonify(error="Username/email and password are required."), 400

    user = User.query.filter(
        (User.username == identifier) | (User.email == identifier.lower())
    ).first()

    if not user or not user.check_password(password):
        return jsonify(error="Invalid username/email or password."), 401

    login_user(user, remember=True)
    return jsonify({"authenticated": True, "user": user.to_dict()}), 200


@auth_bp.post("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
    return jsonify({"authenticated": False, "message": "Signed out successfully."}), 200


@auth_bp.put("/profile")
def update_profile():
    if not current_user.is_authenticated:
        return jsonify(error="Sign in to save profile preferences to your account."), 401

    data = request.get_json(silent=True) or {}
    if "full_name" in data:
        current_user.full_name = str(data["full_name"]).strip()[:120] or current_user.username
    if "farm_location" in data:
        current_user.farm_location = str(data["farm_location"]).strip()[:120]
    if data.get("preferred_theme") in ("light", "forest"):
        current_user.preferred_theme = data["preferred_theme"]
    if data.get("preferred_units") in ("metric", "imperial"):
        current_user.preferred_units = data["preferred_units"]

    db.session.commit()
    return jsonify({"user": current_user.to_dict(), "message": "Profile updated."}), 200
