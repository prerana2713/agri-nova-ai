"""Educational fertilizer knowledge base without unverified dosing instructions."""

FERTILIZER_GUIDE = [
    {
        "id": "urea",
        "name": "Urea",
        "category": "Straight Nitrogen Fertilizer",
        "primary_nutrient": "Nitrogen",
        "composition": "46% Nitrogen (46-0-0)",
        "role": "Concentrated solid nitrogen source supplying amide nitrogen that converts to plant-available ammonium and nitrate in soil.",
        "purpose": "Used when soil tests or crop diagnostics indicate a primary nitrogen deficit for vegetative leaf and stem development.",
        "benefits": [
            "High nitrogen concentration reduces transport volume per unit of nitrogen.",
            "Water-soluble and compatible with soil incorporation or split agricultural programs.",
        ],
        "precautions": [
            "Surface application on warm, moist, or alkaline soils can cause ammonia volatilization loss.",
            "Avoid direct seed contact at planting; over-application risks lodging, excess vegetative growth, and nitrate leaching.",
        ],
        "soil_test_context": "Relevant when laboratory soil tests show low available nitrogen while phosphorus and potassium are already adequate.",
    },
    {
        "id": "dap",
        "name": "DAP (Diammonium Phosphate)",
        "category": "Nitrogen-Phosphorus Compound",
        "primary_nutrient": "Phosphorus",
        "composition": "18% Nitrogen, 46% Phosphorus (P2O5), 0% Potassium (18-46-0)",
        "role": "Supplies concentrated phosphorus alongside starter nitrogen for early root establishment and energy transfer.",
        "purpose": "Commonly selected in pre-plant or basal nutrition when phosphorus is low and a modest starter nitrogen boost is helpful.",
        "benefits": [
            "High water-soluble phosphorus availability supports early seedling vigor and root branching.",
            "Provides dual N + P nutrition in a single granular source.",
        ],
        "precautions": [
            "Creates a temporarily alkaline zone around dissolving granules; avoid heavy concentration directly on germinating seeds.",
            "Excess phosphorus buildup can tie up micronutrients such as zinc and pollute waterways via runoff.",
        ],
        "soil_test_context": "Best considered when soil test phosphorus is low and potassium levels do not require supplementation.",
    },
    {
        "id": "npk-17-17-17",
        "name": "NPK 17-17-17",
        "category": "Balanced Complex NPK",
        "primary_nutrient": "Balanced NPK",
        "composition": "17% N, 17% P2O5, 17% K2O (1:1:1 ratio)",
        "role": "Uniform complex granule delivering equal proportions of all three primary macronutrients.",
        "purpose": "Supports balanced baseline maintenance when N, P, and K are all moderately needed.",
        "benefits": [
            "Every granule contains uniform N, P, and K ratios for even field distribution.",
            "Simplifies multi-nutrient basal management where balanced replenishment is confirmed.",
        ],
        "precautions": [
            "Do not use a balanced grade if only one nutrient is low, as excess nutrients are wasted.",
            "Store in dry conditions to prevent caking.",
        ],
        "soil_test_context": "Appropriate when soil analysis shows balanced or mild simultaneous deficits across N, P, and K.",
    },
    {
        "id": "npk-14-35-14",
        "name": "NPK 14-35-14",
        "category": "High-Phosphorus Complex NPK",
        "primary_nutrient": "Phosphorus",
        "composition": "14% N, 35% P2O5, 14% K2O",
        "role": "Phosphorus-rich complete NPK complex supporting root initiation, flowering, and early establishment.",
        "purpose": "Used in soils notably deficient in phosphorus while still supplying starter nitrogen and potassium.",
        "benefits": [
            "Targets phosphorus limitations while preventing potassium depletion.",
            "Useful for crops establishing strong root systems early in the season.",
        ],
        "precautions": [
            "Avoid unnecessary application on high-phosphorus soils.",
            "Incorporate responsibly to minimize surface erosion loss.",
        ],
        "soil_test_context": "Relevant when phosphorus is markedly low and moderate N and K support are also warranted.",
    },
    {
        "id": "npk-10-26-26",
        "name": "NPK 10-26-26",
        "category": "High P-K Complex NPK",
        "primary_nutrient": "Potassium",
        "composition": "10% N, 26% P2O5, 26% K2O",
        "role": "High phosphorus and potassium complex with modest starter nitrogen for tuber, boll, grain-fill, and stress resilience.",
        "purpose": "Used when soil tests highlight low P and K relative to nitrogen.",
        "benefits": [
            "Supports root strength, water regulation, stalk sturdiness, and reproductive quality.",
            "Limits excessive early nitrogen where vegetative overgrowth is undesirable.",
        ],
        "precautions": [
            "Not intended as a sole nitrogen top-dress during peak vegetative demand.",
            "Verify crop chloride sensitivity if potassium source is muriate-based.",
        ],
        "soil_test_context": "Fits soils with low phosphorus and potassium reserves and moderate existing nitrogen.",
    },
    {
        "id": "npk-20-20",
        "name": "NPK 20-20 (20-20-0)",
        "category": "Balanced N-P Complex",
        "primary_nutrient": "Balanced NPK",
        "composition": "20% N, 20% P2O5, 0% K2O",
        "role": "Equal nitrogen-and-phosphorus complex fertilizer without potassium.",
        "purpose": "Addresses combined N and P needs on soils naturally rich in potassium.",
        "benefits": [
            "Avoids applying unnecessary potassium where soil K is already high.",
            "Promotes both early root development and steady vegetative growth.",
        ],
        "precautions": [
            "Monitor soil potassium over successive seasons to ensure K does not become limiting.",
            "Follow local split-application guidance for nitrogen efficiency.",
        ],
        "soil_test_context": "Suitable when N and P are below target and soil test potassium is already sufficient.",
    },
    {
        "id": "npk-28-28",
        "name": "NPK 28-28 (28-28-0)",
        "category": "High-Analysis N-P Complex",
        "primary_nutrient": "Nitrogen",
        "composition": "28% N, 28% P2O5, 0% K2O",
        "role": "Concentrated equal N-P compound providing both rapid and sustained vegetative and root nutrient support.",
        "purpose": "Used where high-analysis N and P nutrition is preferred and potassium is adequate.",
        "benefits": [
            "Higher nutrient density per bag compared with lower-analysis blends.",
            "Efficient dual supply of N and P during early-to-mid crop establishment.",
        ],
        "precautions": [
            "High nutrient concentration demands careful calibration and placement.",
            "Does not supply potassium or secondary micronutrients unless paired separately.",
        ],
        "soil_test_context": "Considered when both nitrogen and phosphorus are limited in potassium-sufficient soils.",
    },
    {
        "id": "nitrogen-nutrient",
        "name": "Nitrogen (N) — Nutrient Role",
        "category": "Primary Macronutrient",
        "primary_nutrient": "Nitrogen",
        "composition": "Essential component of chlorophyll, amino acids, and plant proteins",
        "role": "Drives leafy vegetative growth, chlorophyll production, photosynthesis, and overall biomass.",
        "purpose": "Core diagnostic nutrient tracked in every soil test because soil nitrogen fluctuates rapidly with rainfall and crop uptake.",
        "benefits": [
            "Supports vigorous canopy growth and healthy green foliage.",
            "Critical for grain protein and overall yield potential.",
        ],
        "precautions": [
            "Deficiency causes older leaves to turn pale yellow (chlorosis) and stunts growth.",
            "Excess nitrogen delays maturity, weakens stems, increases pest susceptibility, and pollutes groundwater.",
        ],
        "soil_test_context": "Evaluate together with organic matter, moisture, and crop stage rather than relying on a single snapshot.",
    },
    {
        "id": "phosphorus-nutrient",
        "name": "Phosphorus (P) — Nutrient Role",
        "category": "Primary Macronutrient",
        "primary_nutrient": "Phosphorus",
        "composition": "Key component of ATP (cellular energy), DNA, and cell membranes",
        "role": "Powers root development, seedling establishment, flowering, seed formation, and energy transfer.",
        "purpose": "Monitored closely in cold, acidic, or highly alkaline soils where phosphorus easily becomes chemically fixed.",
        "benefits": [
            "Promotes deep, resilient root systems early in crop growth.",
            "Supports timely flowering and uniform crop maturity.",
        ],
        "precautions": [
            "Deficiency often appears as stunted growth and purplish tinting on older leaves.",
            "Soil pH outside ~6.0–7.5 sharply reduces phosphorus availability even when total soil P is present.",
        ],
        "soil_test_context": "Interpret soil phosphorus alongside soil pH before selecting a phosphate source.",
    },
    {
        "id": "potassium-nutrient",
        "name": "Potassium (K) — Nutrient Role",
        "category": "Primary Macronutrient",
        "primary_nutrient": "Potassium",
        "composition": "Plant electrolyte regulating stomata, enzyme activation, and water transport",
        "role": "Improves drought tolerance, disease resistance, stalk strength, and carbohydrate/sugar movement.",
        "purpose": "Essential for crop quality, stress resilience, and balancing high nitrogen applications.",
        "benefits": [
            "Reduces lodging and strengthens cell walls.",
            "Regulates stomatal opening for efficient water use.",
        ],
        "precautions": [
            "Deficiency typically shows as scorching or yellowing along older leaf margins.",
            "Sandy soils leach potassium more readily than clay-rich soils.",
        ],
        "soil_test_context": "Review cation exchange capacity (soil texture) and crop residue return when interpreting K.",
    },
    {
        "id": "organic-fertilizers",
        "name": "Organic Fertilizers & Amendments",
        "category": "Soil-Building Amendments",
        "primary_nutrient": "Organic",
        "composition": "Compost, vermicompost, farmyard manure, green manure, and bio-inputs (variable N-P-K)",
        "role": "Builds soil organic matter, improves water-holding capacity, feeds beneficial soil microbes, and releases nutrients gradually.",
        "purpose": "Used as foundational soil conditioners alongside or integrated with mineral nutrient management.",
        "benefits": [
            "Enhances soil structure in both sandy (moisture retention) and clayey (aeration) soils.",
            "Slow nutrient release lowers leaching risk and improves long-term soil fertility.",
        ],
        "precautions": [
            "Nutrient concentrations vary widely; uncomposted manure can introduce weed seeds, pathogens, or temporary nitrogen tie-up.",
            "Release rate depends on soil temperature and moisture, so immediate deficiency correction may take time.",
        ],
        "soil_test_context": "Valuable for low-organic-matter soils and integrated nutrient management plans confirmed by local testing.",
    },
]


def get_fertilizer_guide(search: str = "", nutrient: str = "") -> list[dict]:
    """Filter fertilizer educational records by search query and nutrient category."""
    q = (search or "").strip().lower()
    nut = (nutrient or "").strip().lower()
    items = []
    for entry in FERTILIZER_GUIDE:
        if nut and nut != "all" and entry["primary_nutrient"].lower() != nut:
            continue
        if q:
            haystack = " ".join([
                entry["name"],
                entry["category"],
                entry["primary_nutrient"],
                entry["composition"],
                entry["role"],
                entry["purpose"],
            ]).lower()
            if q not in haystack:
                continue
        items.append(entry)
    return items
