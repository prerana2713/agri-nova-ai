"""Educational crop growth-stage timelines for the 6 supported crops (no dosing)."""

CROP_STAGE_TIMELINES = {
    "Rice": {
        "ph_range": "5.0 – 7.2",
        "moisture_note": "High moisture / controlled paddy water management",
        "stages": [
            {"stage": "1. Nursery & Transplanting", "window": "Weeks 1–3", "focus": "Phosphorus & Root Establishment", "note": "Ensure uniform seedling vigor and gentle early water depth."},
            {"stage": "2. Active Tillering", "window": "Weeks 4–7", "focus": "Nitrogen & Canopy Development", "note": "Monitor leaf color and maintain steady root-zone moisture."},
            {"stage": "3. Panicle Initiation & Flowering", "window": "Weeks 8–12", "focus": "Potassium & Reproductive Support", "note": "Avoid moisture stress during flowering and grain set."},
            {"stage": "4. Grain Fill & Ripening", "window": "Weeks 13–17", "focus": "Drainage & Harvest Readiness", "note": "Gradually reduce standing water prior to physiological maturity."},
        ],
    },
    "Wheat": {
        "ph_range": "6.0 – 7.8",
        "moisture_note": "Well-drained loamy moisture without waterlogging",
        "stages": [
            {"stage": "1. Crown Root Initiation", "window": "Weeks 1–3", "focus": "Phosphorus & Starter N", "note": "Critical early irrigation and root-anchoring stage."},
            {"stage": "2. Tillering & Stem Elongation", "window": "Weeks 4–9", "focus": "Nitrogen & Biomass Growth", "note": "Monitor soil moisture and check for nutrient deficiency symptoms."},
            {"stage": "3. Booting & Flowering", "window": "Weeks 10–13", "focus": "Balanced NPK & Pollination", "note": "Protect against heat stress and maintain moderate soil moisture."},
            {"stage": "4. Grain Filling & Maturity", "window": "Weeks 14–18", "focus": "Potassium & Stalk Strength", "note": "Stop irrigation once kernels reach hard-dough maturity."},
        ],
    },
    "Maize": {
        "ph_range": "5.5 – 7.5",
        "moisture_note": "Moderate steady moisture with good aeration",
        "stages": [
            {"stage": "1. Emergence & V3 Seedling", "window": "Weeks 1–2", "focus": "Phosphorus & Root Vigor", "note": "Sensitive to waterlogging; check seedbed drainage."},
            {"stage": "2. Rapid Vegetative (V6–V12)", "window": "Weeks 3–6", "focus": "Nitrogen & Stalk Growth", "note": "Peak nutrient uptake period; monitor leaf chlorosis."},
            {"stage": "3. Tasseling & Silking", "window": "Weeks 7–10", "focus": "Moisture & Potassium", "note": "Most moisture-sensitive stage for kernel set."},
            {"stage": "4. Grain Fill & Dry-Down", "window": "Weeks 11–15", "focus": "Carbohydrate Translocation", "note": "Inspect stalk strength and harvest at black-layer maturity."},
        ],
    },
    "Cotton": {
        "ph_range": "5.8 – 8.2",
        "moisture_note": "Deep black/loamy moisture retention with drainage",
        "stages": [
            {"stage": "1. Emergence & Seedling", "window": "Weeks 1–3", "focus": "Phosphorus & Taproot Depth", "note": "Avoid crusting and cold saturated soils."},
            {"stage": "2. Squaring & Canopy Growth", "window": "Weeks 4–8", "focus": "Nitrogen & Branching", "note": "Avoid excessive vegetative growth that shades lower bolls."},
            {"stage": "3. Flowering & Boll Set", "window": "Weeks 9–15", "focus": "Potassium & Boll Retention", "note": "Monitor moisture stress and high-humidity pest pressure."},
            {"stage": "4. Boll Opening", "window": "Weeks 16–22", "focus": "Dry Weather & Fiber Quality", "note": "Reduce irrigation so bolls open cleanly."},
        ],
    },
    "Sugarcane": {
        "ph_range": "6.0 – 7.8",
        "moisture_note": "Consistent moisture over a long 10–12 month cycle",
        "stages": [
            {"stage": "1. Germination & Emergence", "window": "Months 1–2", "focus": "Phosphorus & Sett Rooting", "note": "Keep furrow soil moist but not flooded."},
            {"stage": "2. Tillering Phase", "window": "Months 2–4", "focus": "Nitrogen & Tiller Survival", "note": "Earthing up improves aeration and root anchorage."},
            {"stage": "3. Grand Growth Phase", "window": "Months 5–8", "focus": "Balanced NPK & Irrigation", "note": "Peak cane elongation and biomass accumulation."},
            {"stage": "4. Ripening & Sugar Accumulation", "window": "Months 9–12", "focus": "Potassium & Controlled Moisture", "note": "Withhold excess water/nitrogen to support sucrose concentration."},
        ],
    },
    "Groundnut": {
        "ph_range": "5.8 – 7.2",
        "moisture_note": "Friable, well-aerated sandy/red loam",
        "stages": [
            {"stage": "1. Germination & Establishment", "window": "Weeks 1–3", "focus": "Starter P & Nodulation", "note": "Legumes fix atmospheric nitrogen via root nodules."},
            {"stage": "2. Flowering & Pegging", "window": "Weeks 4–7", "focus": "Calcium, P & Loose Surface Soil", "note": "Ensure friable soil surface so pegs penetrate easily."},
            {"stage": "3. Pod Formation & Fill", "window": "Weeks 8–12", "focus": "Potassium & Steady Moisture", "note": "Avoid drought stress during pod filling."},
            {"stage": "4. Pod Maturity", "window": "Weeks 13–16", "focus": "Dry Lifting Window", "note": "Inspect inner shell darkening before harvesting."},
        ],
    },
}


def get_crop_stages(crop: str = "") -> dict:
    if crop and crop in CROP_STAGE_TIMELINES:
        return {"crop": crop, **CROP_STAGE_TIMELINES[crop]}
    return {"crops": CROP_STAGE_TIMELINES}
