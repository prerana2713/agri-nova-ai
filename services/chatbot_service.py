"""Local rule-based agricultural assistant connected to the latest soil analysis."""


def _find_gap(analysis: dict, nutrient_name: str) -> dict | None:
    for gap in analysis.get("gaps") or []:
        if str(gap.get("name", "")).lower() == nutrient_name.lower():
            return gap
    return None


def generate_chat_reply(message: str, latest_analysis: dict | None = None) -> dict:
    """
    Rule-based Agri Nova AI Assistant.
    Uses the latest completed soil analysis when available and transparently
    states its rule-based nature.
    """
    text = (message or "").strip()
    if not text:
        return {
            "reply": "Please enter a question about your soil analysis, NPK nutrients, fertilizers, pH, or crops.",
            "engine": "rule-based",
            "has_analysis_context": bool(latest_analysis),
        }

    q = text.lower()

    # 1. Context-aware queries connected to latest soil analysis
    if any(k in q for k in ["my soil", "my analysis", "latest analysis", "my report", "what is my soil"]):
        if not latest_analysis:
            return {
                "reply": (
                    "No completed soil analysis is loaded yet. Open the Soil Analysis tab, "
                    "submit your soil readings, and then ask me to explain your results!"
                ),
                "engine": "rule-based",
                "has_analysis_context": False,
            }
        gaps_summary = ", ".join(
            f"{g['name']}: {g['status']} ({g['percent']}%)"
            for g in (latest_analysis.get("gaps") or [])
        )
        return {
            "reply": (
                f"Latest Soil Analysis Summary:\n"
                f"• Crop: {latest_analysis.get('crop', 'N/A')} | Soil Type: {latest_analysis.get('soil_type', 'N/A')}\n"
                f"• Demo Soil Match Index: {latest_analysis.get('score', 'N/A')}/100\n"
                f"• ML Fertilizer Prediction: {latest_analysis.get('fertilizer', 'N/A')}\n"
                f"• NPK Status: {gaps_summary or 'Not available'}\n"
                f"• pH: {latest_analysis.get('ph', 'N/A')} | Moisture: {latest_analysis.get('moisture', 'N/A')}%\n\n"
                f"Note: This summary comes directly from your latest session/saved report."
            ),
            "engine": "rule-based",
            "has_analysis_context": True,
        }

    if any(k in q for k in ["fertilizer did", "model predict", "predicted fertilizer", "my fertilizer", "recommendation"]):
        if not latest_analysis:
            return {
                "reply": "You haven't run a soil analysis yet. Run one in Soil Analysis to see the Random Forest fertilizer prediction.",
                "engine": "rule-based",
                "has_analysis_context": False,
            }
        return {
            "reply": (
                f"For {latest_analysis.get('crop')} on {latest_analysis.get('soil_type', 'your')} soil, "
                f"the Random Forest model predicted: **{latest_analysis.get('fertilizer')}**.\n\n"
                f"Remember: this prediction comes from a 99-record academic prototype dataset and is not "
                f"a validated field prescription. Verify product and rate with an agronomist."
            ),
            "engine": "rule-based",
            "has_analysis_context": True,
        }

    if any(k in q for k in ["my nitrogen", "nitrogen status", "my phosphorus", "phosphorus status", "my potassium", "potassium status"]):
        if not latest_analysis:
            return {
                "reply": "Run a Soil Analysis first so I can check your Nitrogen, Phosphorus, and Potassium status.",
                "engine": "rule-based",
                "has_analysis_context": False,
            }
        target_nutrient = (
            "Nitrogen" if "nitrogen" in q
            else "Phosphorus" if "phosphorus" in q
            else "Potassium"
        )
        gap = _find_gap(latest_analysis, target_nutrient)
        if gap:
            return {
                "reply": (
                    f"Your {target_nutrient} status for {latest_analysis.get('crop')} is **{gap['status']}** "
                    f"({gap['percent']}% of the prototype baseline; entered value: {gap.get('value', 'N/A')} kg/ha)."
                ),
                "engine": "rule-based",
                "has_analysis_context": True,
            }

    if any(k in q for k in ["crop did i", "my crop", "selected crop"]):
        if not latest_analysis:
            return {
                "reply": "No crop has been analyzed yet. Choose one of the 6 supported crops in Soil Analysis first.",
                "engine": "rule-based",
                "has_analysis_context": False,
            }
        return {
            "reply": (
                f"Your latest analysis was run for **{latest_analysis.get('crop')}** "
                f"on **{latest_analysis.get('soil_type', 'recorded')}** soil."
            ),
            "engine": "rule-based",
            "has_analysis_context": True,
        }

    if any(k in q for k in ["match index", "my score", "soil score", "explain score", "explain my soil match"]):
        if not latest_analysis:
            return {
                "reply": "Complete a Soil Analysis first, and I will break down your Demo Soil Match Index.",
                "engine": "rule-based",
                "has_analysis_context": False,
            }
        low_items = [g["name"] for g in (latest_analysis.get("gaps") or []) if g.get("status") == "Low"]
        ph_val = latest_analysis.get("ph")
        ph_note = (
            f"pH ({ph_val}) also incurred an 8-point out-of-range check."
            if ph_val is not None and (ph_val < 4.8 or ph_val > 8.5)
            else f"pH ({ph_val}) was within the 4.8–8.5 prototype band."
        )
        low_note = (
            f"Low prototype nutrient flags ({', '.join(low_items)}) reduced the score by 12 points each."
            if low_items
            else "No nutrients were flagged Low under prototype thresholds."
        )
        return {
            "reply": (
                f"Your Demo Soil Match Index is **{latest_analysis.get('score')}/100**.\n"
                f"How this prototype score is calculated: it starts at 92, subtracts 12 for each "
                f"nutrient below 75% of the illustrative crop baseline, and subtracts 8 if pH is below 4.8 or above 8.5.\n"
                f"• {low_note}\n• {ph_note}"
            ),
            "engine": "rule-based",
            "has_analysis_context": True,
        }

    # 2. General rule-based agricultural knowledge base
    if "npk" in q:
        return {
            "reply": (
                "NPK stands for the three primary plant macronutrients:\n"
                "• **Nitrogen (N)**: Supports leafy growth and chlorophyll.\n"
                "• **Phosphorus (P)**: Drives root establishment, energy transfer, and flowering.\n"
                "• **Potassium (K)**: Strengthens stalks, water regulation, and stress resilience.\n"
                "Check the Fertilizer Guide page to compare NPK grades like 17-17-17, 14-35-14, and 10-26-26."
            ),
            "engine": "rule-based",
            "has_analysis_context": bool(latest_analysis),
        }

    if "urea" in q:
        return {
            "reply": (
                "**Urea (46-0-0)** is a concentrated solid nitrogen fertilizer used when soil tests "
                "show a primary nitrogen deficit. To reduce volatilization loss, incorporate it responsibly "
                "or time applications with moisture, and confirm exact rates with a local agronomist."
            ),
            "engine": "rule-based",
            "has_analysis_context": bool(latest_analysis),
        }

    if "dap" in q:
        return {
            "reply": (
                "**DAP (Diammonium Phosphate, 18-46-0)** supplies high phosphorus alongside starter nitrogen, "
                "supporting early root growth. It is commonly used when phosphorus is low on soil tests."
            ),
            "engine": "rule-based",
            "has_analysis_context": bool(latest_analysis),
        }

    if "organic" in q or "compost" in q or "manure" in q:
        return {
            "reply": (
                "**Organic fertilizers & amendments** (compost, vermicompost, farmyard manure, green manure) "
                "improve soil organic matter, water retention, and microbial activity while releasing nutrients gradually."
            ),
            "engine": "rule-based",
            "has_analysis_context": bool(latest_analysis),
        }

    if "nitrogen" in q:
        return {
            "reply": (
                "**Nitrogen (N)** fuels chlorophyll and leafy vegetative growth. Low nitrogen causes older leaves "
                "to yellow, while excess nitrogen can cause lodging and groundwater nitrate leaching."
            ),
            "engine": "rule-based",
            "has_analysis_context": bool(latest_analysis),
        }

    if "phosphorus" in q:
        return {
            "reply": (
                "**Phosphorus (P)** supports early root branching, ATP energy transfer, and seed/flower formation. "
                "Its availability drops sharply if soil pH is very acidic or alkaline."
            ),
            "engine": "rule-based",
            "has_analysis_context": bool(latest_analysis),
        }

    if "potassium" in q:
        return {
            "reply": (
                "**Potassium (K)** regulates plant water balance, strengthens stems, and supports disease and drought tolerance."
            ),
            "engine": "rule-based",
            "has_analysis_context": bool(latest_analysis),
        }

    if "ph" in q:
        return {
            "reply": (
                "**Soil pH** measures acidity/alkalinity on a 0–14 scale. Most crops absorb nutrients best between "
                "**pH 6.0 and 7.5**. Extreme pH locks up phosphorus and micronutrients even if nutrients are present."
            ),
            "engine": "rule-based",
            "has_analysis_context": bool(latest_analysis),
        }

    if "moisture" in q or "irrigation" in q:
        return {
            "reply": (
                "**Soil moisture (%)** reflects available water in the root zone. Too little moisture stresses crops "
                "and reduces nutrient uptake; excess moisture in clayey/black soils can cause root hypoxia and leaching."
            ),
            "engine": "rule-based",
            "has_analysis_context": bool(latest_analysis),
        }

    if any(s in q for s in ["sandy", "loamy", "black", "red", "clayey", "soil type"]):
        return {
            "reply": (
                "Supported soil types in Agri Nova AI:\n"
                "• **Loamy**: Balanced drainage and nutrient retention; ideal for many crops.\n"
                "• **Sandy**: Drains quickly, warms fast, lower nutrient/water holding.\n"
                "• **Clayey**: High water/nutrient retention, slower drainage.\n"
                "• **Black**: Clay-rich moisture retention; classic for cotton and sugarcane.\n"
                "• **Red**: Well-drained, often lower in nitrogen/organic matter; suits groundnut and millets."
            ),
            "engine": "rule-based",
            "has_analysis_context": bool(latest_analysis),
        }

    if any(c in q for c in ["rice", "wheat", "maize", "cotton", "sugarcane", "groundnut", "crop"]):
        return {
            "reply": (
                "The Random Forest model supports 6 crops: **Rice, Wheat, Maize, Cotton, Sugarcane, and Groundnut**. "
                "Try the **Crop Recommendation** module (experimental rule-based prototype) to compare which of these "
                "best matches your soil conditions."
            ),
            "engine": "rule-based",
            "has_analysis_context": bool(latest_analysis),
        }

    if any(f in q for f in ["10-26-26", "14-35-14", "17-17-17", "20-20", "28-28", "fertilizer"]):
        return {
            "reply": (
                "The ML model predicts across 7 fertilizer categories: **Urea, DAP, 10-26-26, 14-35-14, 17-17-17, "
                "20-20, and 28-28**. Open the **Fertilizer Guide** page to search, filter, and compare their compositions and precautions."
            ),
            "engine": "rule-based",
            "has_analysis_context": bool(latest_analysis),
        }

    if any(p in q for p in ["pest", "parasite", "insect", "aphid", "armyworm", "mite", "pesticide", "blight", "rust", "animal", "camera"]):
        return {
            "reply": (
                "Open the **Pest & Camera AI** page to inspect plants, insects, or crop animals using your webcam or an uploaded photo.\n"
                "It runs **3 local ONNX vision models** (PlantDisease 38-class, CerealPestAID 26-class, and ImageNet-1k) "
                "and provides safe **Integrated Pest Management (IPM)** guidance—cultural, biological, and general pesticide classes to confirm with an agronomist."
            ),
            "engine": "rule-based",
            "has_analysis_context": bool(latest_analysis),
        }

    if any(h in q for h in ["hello", "hi", "hey", "help"]):
        return {
            "reply": (
                "Hello! I am the **Agri Nova AI Assistant** (local rule-based knowledge engine). Ask me:\n"
                "• 'What is my soil analysis?' or 'Explain my soil match index'\n"
                "• 'What fertilizer did my model predict?'\n"
                "• 'What is NPK?', 'Explain Urea', 'Soil pH', or 'Soil types'"
            ),
            "engine": "rule-based",
            "has_analysis_context": bool(latest_analysis),
        }

    return {
        "reply": (
            "I'm a rule-based agricultural assistant and didn't match that exact topic. Try asking about:\n"
            "• Your latest soil analysis ('What is my soil analysis?', 'What is my nitrogen status?')\n"
            "• NPK nutrients, Urea, DAP, or Organic fertilizers\n"
            "• Soil pH, soil moisture, soil types (Sandy, Loamy, Black, Red, Clayey), or supported crops."
        ),
        "engine": "rule-based",
        "has_analysis_context": bool(latest_analysis),
    }
