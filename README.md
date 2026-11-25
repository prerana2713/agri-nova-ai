---
title: Agri Nova AI
emoji: 🌱
colorFrom: green
colorTo: emerald
sdk: docker
app_port: 7860
pinned: false
---

# Agri Nova AI

**Precision Agriculture. Smarter Decisions. Sustainable Farming.**

Agri Nova AI is a full-stack Flask + Machine Learning academic prototype web application for soil nutrient analysis, Random Forest fertilizer category prediction, ML explainability, batch CSV analysis, field plot tracking, crop suitability exploration, weather risk advisories, QR-verified PDF reports, and an offline rule-based agricultural assistant.

## Key Features
- **Overview Dashboard & Trend Analytics**: Real KPI metrics from SQLite, latest NPK comparison chart, Soil Match Index historical trend line chart, sustainable farming tips, and a real **Random Forest Feature Importance Model Card** extracted from `fertilizer_model.pkl`.
- **Soil Analysis + Live What-If Simulator**: Preserves the trained `ml_model/fertilizer_model.pkl` pipeline across 6 supported crops (`Rice`, `Wheat`, `Maize`, `Cotton`, `Sugarcane`, `Groundnut`) and 5 soil types (`Sandy`, `Loamy`, `Black`, `Red`, `Clayey`), displaying tree-vote distribution (`predict_proba`), interactive N/P/K/pH What-If sliders, weather-aware field advisory, NPK progress bars, radar chart, and QR-verified PDF/CSV export.
- **Batch CSV Soil Upload**: Download a CSV template, upload multi-row soil samples (validated on backend), optionally save to history, and export predictions to CSV.
- **Field / Plot Profiles**: Create named farm plots in SQLite (`Plot` model), auto-fill soil type during analysis, and filter history by plot.
- **Multi-Report Comparison**: Select 2–4 saved reports in Reports History to compare all soil metrics and ML predictions side by side.
- **Crop Recommendation (Experimental Prototype)**: Transparent, explainable rule-based suitability rubric clearly labeled as an experimental prototype.
- **Pest & Camera AI (Local ONNX Vision + Safe IPM)**: Live webcam capture or photo upload processed offline by 3 local ONNX models (`plant_disease.onnx` 38-class, `cereal_pest.onnx` 26-class, and `animal_mobilenet.onnx` 1000-class) with canopy color metrics and Integrated Pest Management (IPM) pesticide-class awareness.
- **Fertilizer Guide**: Searchable, filterable, and side-by-side comparable knowledge base covering Urea, DAP, NPK grades (`10-26-26`, `14-35-14`, `17-17-17`, `20-20`, `28-28`), Nitrogen, Phosphorus, Potassium, and Organic fertilizers without unsafe application doses.
- **Weather & Field Risk Advisories**: Backend OpenWeatherMap integration via `.env` (`OPENWEATHER_API_KEY`) with clearly labeled Demo Mode fallback and rule-based rain/wind/heat/humidity field advisories.
- **QR-Verified PDF Reports & Sample Bag Tags**: ReportLab A4 PDF reports with an embedded QR verification stamp (`qrcode`), Report ID, NPK chart, health insights, and page numbers, plus printable A6 QR Soil Lab Sample Bag Tags.
- **Live IoT Telemetry & Sensor Stream**: `POST /api/iot/ingest` webhook for ESP32/Arduino sensors plus a clearly labeled Simulated IoT Sensor Stream in Soil Analysis.
- **Dataset Explorer & pH Availability Matrix**: Browse `cleaned_fertilizer_dataset.csv` with 80/20 holdout evaluation caveats, and visualize Soil pH nutrient availability across pH 4.0–9.0.
- **Crop Growth-Stage Timeline & Voice Accessibility**: Interactive 4-stage timelines for all 6 crops, plus Web Speech API microphone input and audio summary playback.
- **Farm Planner, GPS Map & Precision Calculators**: Interactive Leaflet map to pin field plots with lat/lon coordinates and check plot weather, SQLite-backed seasonal scouting task checklist, and deterministic land area / plant spacing / irrigation water volume calculators.
- **Comparison PDF & One-Click Audit ZIP**: Export multi-report side-by-side comparison PDFs (`GET /api/history/compare/pdf`) and full farm audit ZIP bundles (`GET /api/export/audit-zip`).
- **Bilingual / Multilingual UI**: Instant switcher for English (`EN`), Hindi (`हिन्दी`), and Kannada (`ಕನ್ನಡ`).
- **Agri Nova AI Assistant**: Floating bottom-right widget + dedicated Assistant page powered by a local rule-based knowledge base connected to your latest soil analysis.

## Setup & Run Locally (Windows PowerShell)
```powershell
cd "C:\Users\giris\Downloads\Agri_Nova_AI_Professional_Website\Agri Nova AI"
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python app.py
```
Then open **http://127.0.0.1:5000** in your browser.

## Deploy Public Live URL (Hugging Face Spaces — No Card Required)
This repository includes a `Dockerfile` (`port 7860`) and Hugging Face Space metadata header.
1. Create a free account at **https://huggingface.co** (no credit card required).
2. Create a new Space at **https://huggingface.co/new-space** (Name: `agri-nova-ai`, SDK: **Docker → Blank**, Visibility: **Public**).
3. Push this repository to the Space:
   ```powershell
   git remote add space https://huggingface.co/spaces/<your-hf-username>/agri-nova-ai
   git push space main
   ```
4. Once built, your public live URL is `https://<your-hf-username>-agri-nova-ai.hf.space`.

## Deploy Public Live URL (Render Free Tier)
This repository includes `Procfile`, `render.yaml`, `.python-version`, and `gunicorn` in `requirements.txt`.
1. Sign in at **https://dashboard.render.com** with GitHub (`prerana2713`).
2. Click **New + → Blueprint** (or **Web Service**) and select `prerana2713/agri-nova-ai`.
3. Render automatically reads `render.yaml` (`pip install -r requirements.txt` and `gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 120`) and publishes a live `https://<your-app>.onrender.com` URL.

## Academic Prototype Disclaimer
The fertilizer classifier was trained on a small 99-record educational dataset (`ml_model/cleaned_fertilizer_dataset.csv`). Predictions, tree-vote distributions, illustrative nutrient targets, Soil Match Index scores, and rule-based crop/weather advisories are for academic demonstration only and are **not** validated agricultural prescriptions. Always consult a certified soil testing laboratory or qualified agronomist before making farm fertilizer decisions.
