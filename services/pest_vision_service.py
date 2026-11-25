from io import BytesIO
import json
import os
import numpy as np
import onnxruntime as ort
from PIL import Image, UnidentifiedImageError

from config import BASE_DIR

VISION_DIR = BASE_DIR / "ml_model" / "vision"

_SESSIONS = {}
_LABELS = {}

_VISION_DISCLAIMER = (
    "Predictions are generated locally by open-source ONNX models (MobileNetV2 PlantVillage "
    "38-class, MobileNetV3 CerealPestAID 26-class, and MobileNetV2 ImageNet-1k). Lab-trained "
    "models can misclassify cluttered field photos or unfamiliar species. Pesticide classes listed "
    "are educational IPM references only—never apply chemical pesticides or dosages without "
    "confirming with a licensed agronomist and product label."
)

# Educational IPM & safe pesticide-class guidance (no unsafe dosages)
_IPM_RULES = [
    {
        "keywords": ["healthy"],
        "category": "Healthy Crop Tissue",
        "severity": "Low Risk",
        "summary": "The leaf model matched a healthy crop appearance with no primary disease class dominating.",
        "cultural": [
            "Continue routine weekly scouting on leaf undersides and growing tips.",
            "Maintain balanced soil nutrition and avoid excessive nitrogen that attracts sap-suckers.",
        ],
        "biological": ["Conserve natural predators such as ladybird beetles, lacewings, and spiders."],
        "pesticide_class": "No pesticide application indicated. Avoid unnecessary preventive spraying.",
        "precaution": "If symptoms exist on stem or roots not visible in this photo, inspect with an extension specialist.",
    },
    {
        "keywords": ["predators", "ladybug"],
        "category": "Beneficial Natural Enemy",
        "severity": "Beneficial — Protect",
        "summary": "Detected a beneficial predatory insect that naturally suppresses aphids, mites, and soft-bodied pests.",
        "cultural": [
            "Preserve flowering field borders and refugia strips to sustain predator populations.",
        ],
        "biological": ["These organisms ARE your biological control allies—let them feed on pest colonies."],
        "pesticide_class": "Avoid broad-spectrum insecticides (e.g., pyrethroids/organophosphates) that wipe out beneficial predators.",
        "precaution": "Always distinguish beneficial insects from pests before deciding on any spray.",
    },
    {
        "keywords": ["aphid", "greenbug", "lygus", "stink_bug", "leafhopper", "cicada", "whitefly"],
        "category": "Sap-Sucking Insect Pest",
        "severity": "Moderate–High Watch",
        "summary": "Sap-sucking pests pierce phloem tissues, causing leaf curl, honeydew/sooty mold, and virus transmission.",
        "cultural": [
            "Inspect shoot tips and leaf undersides; prune heavily infested shoots in small plots.",
            "Avoid excess nitrogen fertilization, which produces soft, aphid-attractive foliage.",
            "Use yellow sticky traps for population monitoring.",
        ],
        "biological": [
            "Encourage ladybird beetles, hoverfly larvae, lacewings, and parasitic wasps.",
            "Botanical / bio-options: Azadirachtin (neem oil) or potassium salts of fatty acids (insecticidal soap).",
        ],
        "pesticide_class": "Educational reference: Botanical neem/insecticidal soaps or targeted systemic/selective sap-sucker classes if economic thresholds are exceeded.",
        "precaution": "Verify local economic threshold levels, pollinator safety (avoid spraying during bloom), and label rates with an agronomist.",
    },
    {
        "keywords": ["armyworm", "cutworm", "moth", "caterpillar", "borer", "hessian_fly"],
        "category": "Chewing Larvae / Boring Pest",
        "severity": "Moderate–High Watch",
        "summary": "Larval/chewing pests defoliate leaves, cut seedlings at soil level, or bore into stems and ears.",
        "cultural": [
            "Scout early morning or dusk (especially around stem bases for cutworms) and hand-collect egg masses.",
            "Use pheromone traps to track adult moth flights and deep summer plowing between crops.",
        ],
        "biological": [
            "Bio-pesticide class: Bacillus thuringiensis (Bt) formulations or entomopathogenic nematodes/NPVs for early-instar larvae.",
            "Encourage insectivorous birds (perches) and Trichogramma egg parasitoids.",
        ],
        "pesticide_class": "Educational reference: Microbial Bt / spinosyn or diamide/selective lepidopteran classes when threshold damage is confirmed.",
        "precaution": "Late-stage caterpillars are harder to control; confirm exact pest species and pre-harvest interval with an agronomist.",
    },
    {
        "keywords": ["weevil", "beetle", "clickbeetle", "wireworm"],
        "category": "Beetle / Weevil / Soil Larva",
        "severity": "Moderate Watch",
        "summary": "Beetles chew foliage/pods while larvae (such as wireworms) feed on roots and germinating seeds.",
        "cultural": [
            "Rotate host crops with non-host species and remove crop residues harboring overwintering adults.",
            "Prepare fine seedbeds and monitor seedling emergence closely.",
        ],
        "biological": [
            "Entomopathogenic fungi (e.g., Beauveria bassiana / Metarhizium) and ground beetles.",
        ],
        "pesticide_class": "Educational reference: Neem-based antifeedants or approved targeted coleopteran/seed-treatment classes verified locally.",
        "precaution": "Do not treat soil blindly for wireworms without scouting bait traps first.",
    },
    {
        "keywords": ["spider mite", "mite"],
        "category": "Arachnid Plant Parasite (Mites)",
        "severity": "Moderate–High Watch",
        "summary": "Spider mites pierce leaf cells causing fine yellow stippling, bronzing, and webbing on undersides during hot, dry weather.",
        "cultural": [
            "Reduce plant drought stress and dusty conditions along field borders.",
            "Wash small plants or prune heavily webbed leaves.",
        ],
        "biological": [
            "Predatory mites (Phytoseiulus / Amblyseius) and minute pirate bugs.",
            "Horticultural oils or wettable sulfur (check temperature/crop safety).",
        ],
        "pesticide_class": "Educational reference: Specific miticides / acaricides or sulfur/horticultural oil classes (standard insecticides often fail against mites and kill their predators).",
        "precaution": "Avoid sulfur applications during extreme heat (>32 °C) or near oil sprays; verify with an agronomist.",
    },
    {
        "keywords": ["blight", "rust", "mildew", "scab", "rot", "leaf spot", "leaf mold", "scorch", "esca"],
        "category": "Fungal / Oomycete Plant Disease",
        "severity": "Moderate–High Watch",
        "summary": "Fungal and oomycete pathogens cause necrotic spots, powdery coatings, rust pustules, or blights, thriving in humid/wet canopies.",
        "cultural": [
            "Improve canopy airflow, avoid overhead irrigation late in the evening, and remove infected debris.",
            "Use disease-free certified seed and crop rotation with non-hosts.",
        ],
        "biological": [
            "Bio-fungicide agents: Trichoderma spp. or Bacillus subtilis preventive colonizers.",
        ],
        "pesticide_class": "Educational reference: Protectant fungicides (copper/sulfur-based) or targeted systemic fungicide classes rotating FRAC groups to prevent resistance.",
        "precaution": "Fungicides protect healthy tissue—confirm exact pathogen (fungal vs bacterial vs nutrient scorch) before spraying.",
    },
    {
        "keywords": ["bacterial"],
        "category": "Bacterial Plant Disease",
        "severity": "Moderate–High Watch",
        "summary": "Bacterial spots/blights spread via rain splash, contaminated tools, and infected seed, creating water-soaked lesions.",
        "cultural": [
            "Avoid working in fields while foliage is wet; sanitize pruning/harvest tools.",
            "Remove severely affected plants and switch from overhead sprinklers to drip/furrow irrigation.",
        ],
        "biological": ["Beneficial Bacillus-based bio-protectants as preventive support."],
        "pesticide_class": "Educational reference: Fixed copper-based bactericides (note: standard fungal-only fungicides do NOT control bacterial infections).",
        "precaution": "Confirm bacterial diagnosis via an agricultural extension lab; copper overuse can build soil toxicity.",
    },
    {
        "keywords": ["virus", "mosaic", "curl", "greening"],
        "category": "Viral / Vector-Borne Disorder",
        "severity": "High Watch",
        "summary": "Viral and phloem-bacterial diseases (mosaic, leaf curl, citrus greening) cause mottling and curling—chemical sprays cannot cure an already infected plant.",
        "cultural": [
            "Rogue (remove and safely destroy) symptomatic plants early to stop field spread.",
            "Control weeds around field borders that harbor viruses and vectors.",
        ],
        "biological": ["Manage insect vectors (whiteflies, aphids, psyllids) using sticky traps and neem/predators."],
        "pesticide_class": "No chemical cures plant viruses directly; vector management focuses on whitefly/aphid IPM rather than spraying for the virus itself.",
        "precaution": "Verify viral infection vs herbicide drift or nutrient deficiency with an agronomist.",
    },
    {
        "keywords": ["snail", "slug"],
        "category": "Mollusk Plant Pest",
        "severity": "Moderate Watch",
        "summary": "Snails and slugs rasp irregular holes in seedlings and leaves, leaving silvery mucus trails.",
        "cultural": [
            "Clear damp mulch/debris near seedlings and use physical copper tape or hand-picking at dusk.",
        ],
        "biological": ["Encourage ground beetles, frogs, and ducks where compatible."],
        "pesticide_class": "Educational reference: Iron-phosphate-based molluscicide baits (safer profile than metaldehyde for pets/wildlife).",
        "precaution": "Verify bait safety around pets, livestock, and waterways.",
    },
    {
        "keywords": ["mouse", "rat", "vole", "hare", "rabbit", "boar", "hog", "cow", "ox", "buffalo", "goat", "sheep", "deer", "bird", "sparrow", "crow", "pigeon", "finch", "jay", "magpie", "monkey", "elephant", "squirrel"],
        "category": "Vertebrate / Animal Crop Intruder",
        "severity": "Field Protection Watch",
        "summary": "Detected an animal or bird species that can graze seedlings, dig tubers, or damage ripening grain/fruit.",
        "cultural": [
            "Use humane exclusion: perimeter fencing, protective netting over high-value beds, reflective bird tape, or acoustic deterrents.",
            "Eliminate grain spills and burrow cover along field bunds for rodents.",
        ],
        "biological": ["Encourage natural raptor perches (owls/hawks) for rodent suppression."],
        "pesticide_class": "Chemical pesticides are NOT appropriate for wildlife/livestock. Use humane physical exclusion; for severe rodent outbreaks consult local extension officers on safe bait-station rules.",
        "precaution": "Follow local wildlife protection laws and avoid open poison baits that harm non-target animals.",
    },
]


def _get_session(model_key: str):
    if model_key in _SESSIONS:
        return _SESSIONS[model_key]

    filename_map = {
        "plant_disease": "plant_disease.onnx",
        "cereal_pest": "cereal_pest.onnx",
        "animal_mobilenet": "animal_mobilenet.onnx",
    }
    path = VISION_DIR / filename_map[model_key]
    if not path.exists():
        raise FileNotFoundError(f"ONNX model file missing: {path.name}")

    _SESSIONS[model_key] = ort.InferenceSession(
        str(path),
        providers=["CPUExecutionProvider"],
    )
    return _SESSIONS[model_key]


def _get_labels(model_key: str) -> list[str]:
    if model_key in _LABELS:
        return _LABELS[model_key]

    if model_key == "plant_disease":
        cfg = json.loads((VISION_DIR / "plant_disease_config.json").read_text(encoding="utf-8"))
        id2label = cfg["id2label"]
        labels = [id2label[str(i)] for i in range(len(id2label))]
    elif model_key == "cereal_pest":
        lines = (VISION_DIR / "cereal_pest_labels.txt").read_text(encoding="utf-8").splitlines()
        labels = []
        for line in lines:
            parts = line.strip().split(None, 1)
            if len(parts) == 2:
                labels.append(parts[1].replace("_", " ").title())
    else:
        labels = [
            line.strip().title()
            for line in (VISION_DIR / "imagenet_classes.txt").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
    _LABELS[model_key] = labels
    return labels


def _preprocess_image(img: Image.Image, norm_mode: str) -> np.ndarray:
    w, h = img.size
    short = min(w, h)
    scale = 256.0 / max(1, short)
    new_w, new_h = max(224, int(round(w * scale))), max(224, int(round(h * scale)))
    resized = img.resize((new_w, new_h), Image.Resampling.BILINEAR)
    left = (new_w - 224) // 2
    top = (new_h - 224) // 2
    cropped = resized.crop((left, top, left + 224, top + 224))

    arr = np.asarray(cropped, dtype=np.float32) / 255.0
    if norm_mode == "half":
        mean = np.array([0.5, 0.5, 0.5], dtype=np.float32)
        std = np.array([0.5, 0.5, 0.5], dtype=np.float32)
    else:
        mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
        std = np.array([0.229, 0.224, 0.225], dtype=np.float32)

    arr = (arr - mean) / std
    arr = np.transpose(arr, (2, 0, 1))
    return np.expand_dims(arr, axis=0)


def _softmax(logits: np.ndarray) -> np.ndarray:
    x = logits.astype(np.float64)
    x = x - np.max(x)
    exp = np.exp(x)
    return exp / np.sum(exp)


def _run_model(model_key: str, img: Image.Image, top_k: int = 3) -> list[dict]:
    sess = _get_session(model_key)
    labels = _get_labels(model_key)
    norm_mode = "half" if model_key == "plant_disease" else "imagenet"
    tensor = _preprocess_image(img, norm_mode)
    input_name = sess.get_inputs()[0].name
    logits = sess.run(None, {input_name: tensor})[0][0]
    probs = _softmax(logits)
    top_idx = np.argsort(probs)[::-1][:top_k]
    return [
        {
            "label": labels[int(i)] if int(i) < len(labels) else f"Class {int(i)}",
            "confidence_pct": round(float(probs[int(i)]) * 100, 1),
            "model": model_key,
        }
        for i in top_idx
    ]


def _compute_canopy_metrics(img: Image.Image) -> dict:
    """Compute basic RGB color breakdown as a transparent visual inspection aid."""
    small = img.resize((120, 120), Image.Resampling.BILINEAR)
    arr = np.asarray(small, dtype=np.float32)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]

    green_mask = (g > r * 1.08) & (g > b * 1.08) & (g > 45)
    yellow_mask = (r > 130) & (g > 120) & (b < 110) & (~green_mask)
    brown_mask = (r > g) & (g >= b * 0.85) & (r > 55) & (r < 175) & (~green_mask) & (~yellow_mask)

    total = float(arr.shape[0] * arr.shape[1])
    return {
        "green_canopy_pct": round(float(np.sum(green_mask)) / total * 100, 1),
        "yellow_chlorosis_pct": round(float(np.sum(yellow_mask)) / total * 100, 1),
        "brown_lesion_pct": round(float(np.sum(brown_mask)) / total * 100, 1),
    }


def get_ipm_guidance(label: str) -> dict:
    low = (label or "").lower()
    for rule in _IPM_RULES:
        if any(kw in low for kw in rule["keywords"]):
            return {
                "category": rule["category"],
                "severity": rule["severity"],
                "summary": rule["summary"],
                "cultural": rule["cultural"],
                "biological": rule["biological"],
                "pesticide_class": rule["pesticide_class"],
                "precaution": rule["precaution"],
            }
    return {
        "category": "General Field Observation",
        "severity": "Inspect Further",
        "summary": (
            f"Classified visually as '{label}'. Confirm whether an insect, animal, disease, "
            "or background object is the main subject before taking action."
        ),
        "cultural": [
            "Capture a close-up photo in clear daylight focused directly on the affected leaf, insect, or animal.",
            "Check multiple plants across the field before deciding on intervention.",
        ],
        "biological": ["Preserve beneficial insects such as ladybirds, spiders, and parasitic wasps."],
        "pesticide_class": "Do not apply pesticides based on an uncertain visual match. Consult a local agronomist.",
        "precaution": "Follow integrated pest management (IPM) thresholds and certified product labels.",
    }


def analyze_pest_image(image_bytes: bytes, mode: str = "auto_hybrid", crop: str = "") -> dict:
    """Validate image bytes, run local ONNX neural networks, and return IPM guidance."""
    if not image_bytes:
        raise ValueError("Uploaded image is empty.")
    if len(image_bytes) > 6 * 1024 * 1024:
        raise ValueError("Image exceeds the 6 MB upload limit.")

    try:
        probe = Image.open(BytesIO(image_bytes))
        probe.verify()
        img = Image.open(BytesIO(image_bytes)).convert("RGB")
    except (UnidentifiedImageError, OSError) as exc:
        raise ValueError("Invalid or unsupported image file. Use JPG, PNG, or WEBP.") from exc

    allowed_modes = {"auto_hybrid", "insect_pest", "leaf_disease", "animal_wildlife"}
    clean_mode = mode if mode in allowed_modes else "auto_hybrid"

    model_results = {}
    if clean_mode == "leaf_disease":
        model_results["plant_disease"] = _run_model("plant_disease", img, top_k=3)
        primary = model_results["plant_disease"][0]
    elif clean_mode == "insect_pest":
        model_results["cereal_pest"] = _run_model("cereal_pest", img, top_k=3)
        primary = model_results["cereal_pest"][0]
    elif clean_mode == "animal_wildlife":
        model_results["animal_mobilenet"] = _run_model("animal_mobilenet", img, top_k=3)
        primary = model_results["animal_mobilenet"][0]
    else:
        # Auto hybrid runs all 3 local ONNX models and picks highest-confidence match
        model_results["plant_disease"] = _run_model("plant_disease", img, top_k=3)
        model_results["cereal_pest"] = _run_model("cereal_pest", img, top_k=3)
        model_results["animal_mobilenet"] = _run_model("animal_mobilenet", img, top_k=3)

        candidates = [
            model_results["plant_disease"][0],
            model_results["cereal_pest"][0],
            model_results["animal_mobilenet"][0],
        ]
        primary = max(candidates, key=lambda x: x["confidence_pct"])

    model_names = {
        "plant_disease": "MobileNetV2 PlantDisease (38-class ONNX)",
        "cereal_pest": "MobileNetV3 CerealPestAID (26-class ONNX)",
        "animal_mobilenet": "MobileNetV2 ImageNet-1k (1000-class ONNX)",
    }

    ipm = get_ipm_guidance(primary["label"])
    canopy = _compute_canopy_metrics(img)

    return {
        "mode": clean_mode,
        "crop_context": crop or "Not specified",
        "primary_prediction": {
            "label": primary["label"],
            "confidence_pct": primary["confidence_pct"],
            "model_used": model_names.get(primary["model"], primary["model"]),
        },
        "model_breakdown": {
            model_names[k]: v for k, v in model_results.items()
        },
        "canopy_metrics": canopy,
        "ipm_guidance": ipm,
        "disclaimer": _VISION_DISCLAIMER,
    }


def get_pest_reference_guide() -> list[dict]:
    """Offline searchable IPM guide for common pests, parasites, diseases, and animals."""
    return [
        {
            "id": f"ipm-{idx + 1}",
            "category": rule["category"],
            "severity": rule["severity"],
            "examples": ", ".join(rule["keywords"][:5]).title(),
            "summary": rule["summary"],
            "cultural": rule["cultural"],
            "biological": rule["biological"],
            "pesticide_class": rule["pesticide_class"],
            "precaution": rule["precaution"],
        }
        for idx, rule in enumerate(_IPM_RULES)
    ]
