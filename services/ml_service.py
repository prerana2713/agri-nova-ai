import os
import joblib
import pandas as pd

from config import Config

_MODEL = None
_MODEL_INSIGHTS = None


def get_model():
    """Load and cache the trained Random Forest pipeline."""
    global _MODEL
    if _MODEL is None:
        _MODEL = joblib.load(Config.MODEL_PATH)
    return _MODEL


def get_model_insights() -> dict:
    """Extract real Random Forest feature importances and dataset statistics."""
    global _MODEL_INSIGHTS
    if _MODEL_INSIGHTS is not None:
        return _MODEL_INSIGHTS

    model = get_model()
    grouped_importance: dict[str, float] = {
        "Nitrogen": 0.0,
        "Phosphorous": 0.0,
        "Potassium": 0.0,
        "Moisture": 0.0,
        "Humidity": 0.0,
        "Temperature": 0.0,
        "Soil Type": 0.0,
        "Crop Type": 0.0,
    }

    try:
        preprocessor = model.named_steps.get("preprocessor")
        classifier = model.named_steps.get("classifier")
        if preprocessor is not None and classifier is not None:
            raw_names = list(preprocessor.get_feature_names_out())
            importances = list(classifier.feature_importances_)
            for feat_name, imp in zip(raw_names, importances):
                clean = feat_name.split("__", 1)[-1]
                if clean.startswith("Soil Type_"):
                    grouped_importance["Soil Type"] += float(imp)
                elif clean.startswith("Crop Type_"):
                    grouped_importance["Crop Type"] += float(imp)
                elif clean in grouped_importance:
                    grouped_importance[clean] += float(imp)
                else:
                    grouped_importance[clean] = grouped_importance.get(clean, 0.0) + float(imp)
    except Exception:
        pass

    feature_list = sorted(
        [
            {"feature": k, "importance_pct": round(v * 100, 1)}
            for k, v in grouped_importance.items()
        ],
        key=lambda item: item["importance_pct"],
        reverse=True,
    )

    dataset_stats = {
        "rows": 0,
        "fertilizer_classes": [str(c) for c in getattr(model, "classes_", [])],
        "fertilizer_counts": {},
        "soil_counts": {},
        "crop_counts": {},
    }
    if os.path.exists(Config.DATASET_PATH):
        try:
            df = pd.read_csv(Config.DATASET_PATH)
            df.columns = df.columns.str.strip()
            dataset_stats["rows"] = int(len(df))
            if "Fertilizer Name" in df.columns:
                dataset_stats["fertilizer_counts"] = {
                    str(k): int(v) for k, v in df["Fertilizer Name"].astype(str).str.strip().value_counts().items()
                }
            if "Soil Type" in df.columns:
                dataset_stats["soil_counts"] = {
                    str(k): int(v) for k, v in df["Soil Type"].astype(str).str.strip().value_counts().items()
                }
            if "Crop Type" in df.columns:
                dataset_stats["crop_counts"] = {
                    str(k): int(v) for k, v in df["Crop Type"].astype(str).str.strip().value_counts().items()
                }
        except Exception:
            pass

    clf = model.named_steps.get("classifier") if hasattr(model, "named_steps") else None
    _MODEL_INSIGHTS = {
        "algorithm": "Random Forest Classifier",
        "n_estimators": int(getattr(clf, "n_estimators", 100)) if clf is not None else 100,
        "feature_importances": feature_list,
        "dataset": dataset_stats,
        "transparency_note": (
            "Feature importances are extracted directly from the trained scikit-learn "
            "Random Forest pipeline. Because the training dataset contains 99 records, "
            "tree-vote splits reflect model behavior on that academic dataset—not real-world accuracy."
        ),
    }
    return _MODEL_INSIGHTS


def _parse_float(data: dict, key: str, label: str, min_val: float, max_val: float) -> float:
    if key not in data or data[key] is None or str(data[key]).strip() == "":
        raise ValueError(f"{label} is required.")
    try:
        value = float(data[key])
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be a valid number.") from exc
    if not (min_val <= value <= max_val):
        raise ValueError(f"{label} must be between {min_val} and {max_val}.")
    return round(value, 2)


def validate_soil_payload(data: dict, require_crop: bool = True) -> dict:
    """Validate incoming soil analysis or crop recommendation request data."""
    if not isinstance(data, dict):
        raise ValueError("Invalid JSON request body.")

    crop = str(data.get("crop", "")).strip()
    if require_crop:
        if crop not in Config.CROP_TARGETS:
            raise ValueError("Select a valid crop.")
        if crop not in Config.CROP_MAPPING:
            raise ValueError(
                "The ML model has not been trained for this crop. "
                "Choose Rice, Wheat, Maize, Cotton, Sugarcane, or Groundnut."
            )

    soil_type = str(data.get("soil_type", "")).strip()
    if soil_type not in Config.ALLOWED_SOILS:
        raise ValueError(
            "Select a valid soil type: Sandy, Loamy, Black, Red, or Clayey."
        )

    temp_unit = str(data.get("temp_unit", "C")).strip().upper()
    raw_temp = data.get("temperature")
    if raw_temp is None or str(raw_temp).strip() == "":
        raise ValueError("Temperature is required.")
    try:
        temperature_val = float(raw_temp)
    except (TypeError, ValueError) as exc:
        raise ValueError("Temperature must be a valid number.") from exc

    if temp_unit == "F":
        temperature_c = round((temperature_val - 32.0) * 5.0 / 9.0, 2)
    else:
        temperature_c = round(temperature_val, 2)

    if not (0 <= temperature_c <= 60):
        raise ValueError("Temperature must be between 0 and 60 °C (32 to 140 °F).")

    humidity = _parse_float(data, "humidity", "Humidity", 0, 100)
    moisture = _parse_float(data, "moisture", "Soil moisture", 0, 100)
    nitrogen = _parse_float(data, "nitrogen", "Nitrogen", 0, 500)
    phosphorus = _parse_float(data, "phosphorus", "Phosphorus", 0, 500)
    potassium = _parse_float(data, "potassium", "Potassium", 0, 500)
    ph = _parse_float(data, "ph", "Soil pH", 0, 14)

    return {
        "crop": crop,
        "soil_type": soil_type,
        "temperature": temperature_c,
        "humidity": humidity,
        "moisture": moisture,
        "nitrogen": nitrogen,
        "phosphorus": phosphorus,
        "potassium": potassium,
        "ph": ph,
    }


def analyze_soil_sample(data: dict) -> tuple[dict, dict]:
    """Validate inputs, run the existing Random Forest model, and build analysis output."""
    inputs = validate_soil_payload(data, require_crop=True)
    model = get_model()

    sample = pd.DataFrame([{
        "Temperature": inputs["temperature"],
        "Humidity": inputs["humidity"],
        "Moisture": inputs["moisture"],
        "Soil Type": inputs["soil_type"],
        "Crop Type": Config.CROP_MAPPING[inputs["crop"]],
        "Nitrogen": inputs["nitrogen"],
        "Potassium": inputs["potassium"],
        "Phosphorous": inputs["phosphorus"],
    }])

    prediction = str(model.predict(sample)[0])

    # Extract real Random Forest tree-vote split across classes
    tree_votes = []
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(sample)[0]
        classes = [str(c) for c in getattr(model, "classes_", [])]
        tree_votes = sorted(
            [
                {"fertilizer": cls, "tree_share_pct": round(float(p) * 100, 1)}
                for cls, p in zip(classes, probs)
                if float(p) > 0
            ],
            key=lambda x: x["tree_share_pct"],
            reverse=True,
        )[:4]

    values = {
        "Nitrogen": inputs["nitrogen"],
        "Phosphorus": inputs["phosphorus"],
        "Potassium": inputs["potassium"],
    }
    targets = Config.CROP_TARGETS[inputs["crop"]]
    names = ["Nitrogen", "Phosphorus", "Potassium"]

    gaps = []
    low = []
    for name, target in zip(names, targets):
        value = values[name]
        status = (
            "Low" if value < target * 0.75
            else "High" if value > target * 1.25
            else "Near demo target"
        )
        percent = min(100, max(0, round(value / target * 100)))
        gaps.append({
            "name": name,
            "value": value,
            "target": target,
            "status": status,
            "percent": percent,
        })
        if status == "Low":
            low.append(name)

    actions = []
    if low:
        actions.append(
            "Review " + ", ".join(low) + " against a certified laboratory soil test."
        )
    else:
        actions.append(
            "No major NPK gap is flagged by the illustrative demonstration thresholds."
        )

    actions.append(
        f"Check crop-specific pH suitability for {inputs['crop']}. Entered pH: {inputs['ph']}."
    )
    actions.append(
        f"Review irrigation and drainage for {inputs['soil_type']} soil at {inputs['moisture']}% moisture."
    )

    ph = inputs["ph"]
    score = max(
        30,
        92 - len(low) * 12 - (8 if ph < 4.8 or ph > 8.5 else 0),
    )

    attention_count = sum(1 for item in gaps if item["status"] in ("Low", "High"))
    if attention_count:
        health_overall = "Further review recommended"
        health_note = (
            f"{attention_count} nutrient parameter(s) need attention under the "
            "illustrative prototype thresholds."
        )
    else:
        health_overall = "No major NPK flags"
        health_note = (
            "No major NPK flags were found using the illustrative prototype thresholds."
        )

    health_observations = [
        {
            "title": item["name"],
            "status": item["status"],
            "detail": (
                f"Entered value: {values[item['name']]} kg/ha "
                f"(prototype reference: ~{item['target']} kg/ha). "
                "Compare with a certified soil test."
            ),
        }
        for item in gaps
    ]
    health_observations.append({
        "title": "Soil pH",
        "status": "Recorded" if 5.5 <= ph <= 7.8 else "Check range",
        "detail": (
            f"Entered pH: {ph}. Verify the suitable range for {inputs['crop']} "
            "using local agricultural guidance."
        ),
    })
    health_observations.append({
        "title": "Soil moisture",
        "status": "Recorded",
        "detail": (
            f"Entered moisture: {inputs['moisture']}%. Interpret this reading "
            f"using {inputs['soil_type']} soil texture and crop growth stage."
        ),
    })

    result = {
        "crop": inputs["crop"],
        "soil_type": inputs["soil_type"],
        "score": score,
        "gaps": gaps,
        "health": {
            "overall": health_overall,
            "note": health_note,
            "observations": health_observations,
        },
        "actions": actions,
        "fertilizer": prediction,
        "tree_vote_distribution": tree_votes,
        "summary": "ML fertilizer prediction completed",
        "model_info": {
            "algorithm": "Random Forest Classifier",
            "dataset_note": "99-record cleaned academic dataset",
            "is_prototype": True,
        },
        "disclaimer": Config.PROTOTYPE_DISCLAIMER,
    }
    return inputs, result


_CROP_PROFILES = {
    "Rice": {
        "soils": ["Clayey", "Loamy", "Black"],
        "temp": (20, 36),
        "humidity": (60, 95),
        "moisture": (45, 90),
        "ph": (5.0, 7.2),
        "npk_min": (40, 20, 20),
        "note": "Prefers water-retentive clayey or loamy soils, warm temperatures, and higher moisture.",
        "considerations": [
            "Ensure bunding or irrigation management matches paddy growth stages.",
            "Monitor standing water and drainage to prevent root hypoxia.",
        ],
    },
    "Wheat": {
        "soils": ["Loamy", "Clayey", "Black"],
        "temp": (12, 26),
        "humidity": (35, 70),
        "moisture": (30, 65),
        "ph": (6.0, 7.8),
        "npk_min": (50, 25, 20),
        "note": "Thrives in well-drained loamy soils with cooler to moderate temperatures and neutral pH.",
        "considerations": [
            "Avoid waterlogged fields during early tillering.",
            "Verify sowing window temperature in your region.",
        ],
    },
    "Maize": {
        "soils": ["Loamy", "Sandy", "Red"],
        "temp": (18, 34),
        "humidity": (45, 80),
        "moisture": (35, 70),
        "ph": (5.5, 7.5),
        "npk_min": (50, 25, 25),
        "note": "Performs well in fertile, well-drained loamy or sandy-loam soils with moderate warmth.",
        "considerations": [
            "Maize is sensitive to poor drainage during early growth.",
            "Confirm hybrid maturity duration with local extension services.",
        ],
    },
    "Cotton": {
        "soils": ["Black", "Loamy", "Red"],
        "temp": (22, 38),
        "humidity": (40, 75),
        "moisture": (30, 65),
        "ph": (5.8, 8.2),
        "npk_min": (40, 20, 25),
        "note": "Well suited to black cotton soils and warm climates with moderate humidity.",
        "considerations": [
            "Excessive late-season humidity can increase bollworm or fungal pressure.",
            "Maintain balanced potassium and drainage in heavy black soils.",
        ],
    },
    "Sugarcane": {
        "soils": ["Loamy", "Black", "Clayey"],
        "temp": (22, 38),
        "humidity": (55, 85),
        "moisture": (45, 80),
        "ph": (6.0, 7.8),
        "npk_min": (60, 30, 30),
        "note": "Requires deep, fertile loamy/black soils, warm conditions, and steady moisture availability.",
        "considerations": [
            "Long-duration crop requiring split nutrient planning based on lab tests.",
            "Avoid prolonged moisture stress during grand growth phase.",
        ],
    },
    "Groundnut": {
        "soils": ["Sandy", "Red", "Loamy"],
        "temp": (22, 35),
        "humidity": (40, 75),
        "moisture": (25, 60),
        "ph": (5.8, 7.2),
        "npk_min": (15, 25, 25),
        "note": "Favors friable sandy or red loamy soils so pegs can penetrate easily without waterlogging.",
        "considerations": [
            "Heavy clayey soils can hinder pod development and harvesting.",
            "Check calcium availability and soil pH prior to flowering.",
        ],
    },
}


def recommend_crops_prototype(data: dict) -> dict:
    """Transparent rule-based crop recommendation prototype."""
    inputs = validate_soil_payload(data, require_crop=False)
    ranked = []

    for crop_name, profile in _CROP_PROFILES.items():
        points = 0
        reasons = []
        gaps = []

        if inputs["soil_type"] in profile["soils"]:
            points += 25
            reasons.append(f"{inputs['soil_type']} soil matches typical {crop_name} soil preference.")
        else:
            gaps.append(
                f"{inputs['soil_type']} soil is less typical for {crop_name} "
                f"(prefers {', '.join(profile['soils'])})."
            )

        t_min, t_max = profile["temp"]
        if t_min <= inputs["temperature"] <= t_max:
            points += 15
            reasons.append(f"Temperature ({inputs['temperature']} °C) is within {t_min}–{t_max} °C.")
        else:
            gaps.append(f"Temperature ({inputs['temperature']} °C) falls outside {t_min}–{t_max} °C.")

        h_min, h_max = profile["humidity"]
        if h_min <= inputs["humidity"] <= h_max:
            points += 10
            reasons.append(f"Humidity ({inputs['humidity']}%) fits the {h_min}–{h_max}% band.")
        else:
            gaps.append(f"Humidity ({inputs['humidity']}%) is outside {h_min}–{h_max}%.")

        m_min, m_max = profile["moisture"]
        if m_min <= inputs["moisture"] <= m_max:
            points += 15
            reasons.append(f"Soil moisture ({inputs['moisture']}%) suits {m_min}–{m_max}%.")
        else:
            gaps.append(f"Soil moisture ({inputs['moisture']}%) is outside {m_min}–{m_max}%.")

        p_min, p_max = profile["ph"]
        if p_min <= inputs["ph"] <= p_max:
            points += 15
            reasons.append(f"Soil pH ({inputs['ph']}) is inside {p_min}–{p_max}.")
        else:
            gaps.append(f"Soil pH ({inputs['ph']}) sits outside {p_min}–{p_max}.")

        n_req, p_req, k_req = profile["npk_min"]
        npk_hits = sum([
            1 if inputs["nitrogen"] >= n_req else 0,
            1 if inputs["phosphorus"] >= p_req else 0,
            1 if inputs["potassium"] >= k_req else 0,
        ])
        points += round((npk_hits / 3) * 20)
        if npk_hits == 3:
            reasons.append("Entered N, P, and K meet minimum prototype baseline levels.")
        else:
            gaps.append(
                f"Entered NPK ({inputs['nitrogen']}/{inputs['phosphorus']}/{inputs['potassium']}) "
                f"partially meets baseline ({n_req}/{p_req}/{k_req} kg/ha)."
            )

        ranked.append({
            "crop": crop_name,
            "suitability_score": points,
            "score_basis": "Matched points out of 100 (Soil 25, Temp 15, Moisture 15, pH 15, Humidity 10, NPK 20).",
            "summary": profile["note"],
            "reasons": reasons,
            "mismatches": gaps,
            "considerations": profile["considerations"],
        })

    ranked.sort(key=lambda item: item["suitability_score"], reverse=True)
    top = ranked[0]

    soil_summary = (
        f"{inputs['soil_type']} soil at {inputs['temperature']} °C, "
        f"{inputs['humidity']}% humidity, {inputs['moisture']}% moisture, "
        f"pH {inputs['ph']}, and NPK ({inputs['nitrogen']}-{inputs['phosphorus']}-{inputs['potassium']})."
    )

    return {
        "prototype_label": "Experimental Rule-Based Prototype — Not a validated ML agronomic model",
        "suggested_crop": top["crop"],
        "suitability_score": top["suitability_score"],
        "score_basis": top["score_basis"],
        "reason": " ".join(top["reasons"]) if top["reasons"] else top["summary"],
        "soil_condition_summary": soil_summary,
        "considerations": top["considerations"] + top["mismatches"],
        "top_matches": ranked[:3],
        "all_candidates": ranked,
        "inputs": inputs,
        "disclaimer": (
            "Experimental prototype using transparent rule-based heuristics over 6 supported crops. "
            "It is not a validated predictive agricultural model. Consult local agronomists, "
            "seasonal calendars, and certified soil tests before selecting a crop."
        ),
    }


def get_dataset_explorer(crop_filter: str = "", fertilizer_filter: str = "") -> dict:
    """Return real dataset records, class breakdown, and 80/20 evaluation metrics with caveats."""
    if not os.path.exists(Config.DATASET_PATH):
        raise FileNotFoundError("Dataset file not found.")

    df = pd.read_csv(Config.DATASET_PATH)
    df.columns = df.columns.str.strip()
    df.rename(columns={"Temparature": "Temperature"}, inplace=True)
    for col in ("Soil Type", "Crop Type", "Fertilizer Name"):
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    from sklearn.metrics import accuracy_score
    from sklearn.model_selection import train_test_split

    X = df.drop("Fertilizer Name", axis=1)
    y = df["Fertilizer Name"]
    _, X_test, _, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    model = get_model()
    y_pred = model.predict(X_test)
    holdout_acc = round(float(accuracy_score(y_test, y_pred)) * 100, 1)

    filtered = df.copy()
    if crop_filter and crop_filter.lower() != "all":
        mapped = Config.CROP_MAPPING.get(crop_filter, crop_filter)
        filtered = filtered[filtered["Crop Type"].str.lower() == mapped.lower()]
    if fertilizer_filter and fertilizer_filter.lower() != "all":
        filtered = filtered[filtered["Fertilizer Name"].str.lower() == fertilizer_filter.lower()]

    rows = []
    for idx, row in filtered.head(40).iterrows():
        rows.append({
            "row_id": int(idx) + 1,
            "temperature": float(row["Temperature"]),
            "humidity": float(row["Humidity"]),
            "moisture": float(row["Moisture"]),
            "soil_type": str(row["Soil Type"]),
            "crop_type": str(row["Crop Type"]),
            "nitrogen": float(row["Nitrogen"]),
            "phosphorous": float(row["Phosphorous"]),
            "potassium": float(row["Potassium"]),
            "fertilizer": str(row["Fertilizer Name"]),
        })

    return {
        "total_rows": int(len(df)),
        "filtered_rows": int(len(filtered)),
        "test_split_rows": int(len(X_test)),
        "holdout_accuracy_pct": holdout_acc,
        "fertilizer_counts": {
            str(k): int(v) for k, v in df["Fertilizer Name"].value_counts().items()
        },
        "soil_counts": {
            str(k): int(v) for k, v in df["Soil Type"].value_counts().items()
        },
        "crop_counts": {
            str(k): int(v) for k, v in df["Crop Type"].value_counts().items()
        },
        "rows": rows,
        "validation_caveat": (
            f"Holdout accuracy ({holdout_acc}% on {len(X_test)} test samples from a 99-record "
            "academic dataset) measures fit to this small educational dataset only. It does NOT "
            "represent real-world agronomic accuracy across diverse soils, climates, or regions."
        ),
    }
