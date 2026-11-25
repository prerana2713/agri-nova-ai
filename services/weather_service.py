from datetime import datetime
import requests

from config import Config

_DEMO_WEATHER_PROFILES = {
    "bengaluru": (25.4, 68, "Partly Cloudy", 11.5, 25),
    "delhi": (29.2, 42, "Clear Sky", 9.8, 5),
    "mumbai": (31.0, 76, "Humid & Breezy", 16.2, 65),
    "chennai": (32.5, 74, "Scattered Clouds", 14.4, 30),
    "hyderabad": (28.8, 55, "Mostly Sunny", 10.5, 10),
    "pune": (26.7, 58, "Mild Breeze", 12.1, 15),
    "ludhiana": (24.1, 49, "Clear & Dry", 8.6, 5),
}


def build_weather_advisories(weather_data: dict) -> list[dict]:
    """Generate transparent rule-based agricultural weather advisories."""
    advisories = []
    rain = float(weather_data.get("rain_probability", 0) or 0)
    wind = float(weather_data.get("wind_speed_kmh", 0) or 0)
    temp = float(weather_data.get("temperature_c", 25) or 25)
    humidity = float(weather_data.get("humidity", 50) or 50)

    if rain >= 50:
        advisories.append({
            "level": "warning",
            "title": "Elevated Rain Risk — Nutrient Runoff Caution",
            "detail": (
                f"Rain probability is {round(rain)}%. Surface-applied nutrients can leach or wash away "
                "during heavy rainfall; verify field drainage and local timing guidance."
            ),
        })
    if wind >= 20:
        advisories.append({
            "level": "warning",
            "title": "Breezy Conditions — Drift Caution",
            "detail": (
                f"Wind speed is {wind:.1f} km/h. Avoid broadcasting fine inputs or foliar sprays during gusty hours."
            ),
        })
    if temp >= 34:
        advisories.append({
            "level": "caution",
            "title": "High Temperature — Volatilization & Moisture Stress",
            "detail": (
                f"Temperature is {temp:.1f} °C. Warm surface soils increase nitrogen volatilization risk "
                "and evapotranspiration; monitor soil moisture closely."
            ),
        })
    if humidity >= 80:
        advisories.append({
            "level": "info",
            "title": "High Humidity — Crop Scouting Reminder",
            "detail": (
                f"Humidity is {round(humidity)}%. Dense canopies in humid conditions benefit from regular foliar disease checks."
            ),
        })
    if not advisories:
        advisories.append({
            "level": "ok",
            "title": "Favorable Field Weather Window",
            "detail": (
                "No extreme rain, wind, or heat risk is flagged by the prototype weather thresholds. "
                "Always confirm with local agricultural bulletins."
            ),
        })
    return advisories


def _demo_weather_response(city: str, reason: str, setup_required: bool) -> dict:
    clean_city = city.strip() or "Bengaluru"
    key = clean_city.lower()
    temp, humidity, cond, wind, rain_prob = _DEMO_WEATHER_PROFILES.get(
        key, (27.5, 62, "Partly Cloudy", 11.0, 20)
    )
    forecast = [
        {"label": "+3h", "temp_c": round(temp + 1.1, 1), "condition": cond, "rain_prob": rain_prob},
        {"label": "+6h", "temp_c": round(temp - 0.8, 1), "condition": cond, "rain_prob": min(95, rain_prob + 5)},
        {"label": "+9h", "temp_c": round(temp - 2.3, 1), "condition": "Clear / Cool", "rain_prob": max(5, rain_prob - 5)},
        {"label": "+12h", "temp_c": round(temp - 3.1, 1), "condition": "Calm", "rain_prob": max(5, rain_prob - 10)},
        {"label": "+24h", "temp_c": round(temp + 0.4, 1), "condition": cond, "rain_prob": rain_prob},
    ]
    payload = {
        "is_live": False,
        "mode": "demo",
        "setup_required": setup_required,
        "status_message": reason,
        "city": clean_city.title(),
        "country": "IN (Demo)",
        "temperature_c": temp,
        "feels_like_c": round(temp + 0.8, 1),
        "humidity": humidity,
        "condition": cond,
        "description": f"{cond} (Illustrative demo data)",
        "wind_speed_kmh": wind,
        "rain_probability": rain_prob,
        "forecast": forecast,
        "updated_at": datetime.now().strftime("%d %b %Y, %I:%M %p"),
        "setup_instructions": (
            "To enable live weather, create a free OpenWeatherMap API key and set "
            "OPENWEATHER_API_KEY=your_key in your .env file, then restart python app.py."
        ),
    }
    payload["advisories"] = build_weather_advisories(payload)
    return payload


def fetch_weather(city: str, lat: float | None = None, lon: float | None = None) -> tuple[dict, int]:
    """Fetch live weather from OpenWeatherMap via backend (city or lat/lon) or return labeled demo mode."""
    query_city = (city or "").strip() or "Bengaluru"
    if len(query_city) > 80:
        return {"error": "City name is too long."}, 400

    api_key = Config.OPENWEATHER_API_KEY
    if not api_key:
        label = query_city if city else (f"Coords ({lat:.2f}, {lon:.2f})" if lat is not None and lon is not None else "Bengaluru")
        return _demo_weather_response(
            label,
            "Demo Mode: OPENWEATHER_API_KEY is not configured on the backend.",
            setup_required=True,
        ), 200

    try:
        base_params = {"appid": api_key, "units": "metric"}
        if lat is not None and lon is not None:
            base_params.update({"lat": lat, "lon": lon})
        else:
            base_params["q"] = query_city

        current_resp = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params=base_params,
            timeout=Config.WEATHER_TIMEOUT_SECONDS,
        )

        if current_resp.status_code == 404:
            return {"error": f"City '{query_city}' was not found. Check spelling and try again."}, 404
        if current_resp.status_code == 401:
            return {
                "error": "Configured OPENWEATHER_API_KEY was rejected (401 Unauthorized).",
                "is_live": False,
                "setup_required": True,
            }, 502
        current_resp.raise_for_status()
        cur = current_resp.json()

        forecast_items = []
        rain_probability = 0
        try:
            fc_resp = requests.get(
                "https://api.openweathermap.org/data/2.5/forecast",
                params={**base_params, "cnt": 5},
                timeout=Config.WEATHER_TIMEOUT_SECONDS,
            )
            if fc_resp.ok:
                fc_json = fc_resp.json()
                for entry in fc_json.get("list", [])[:5]:
                    pop_pct = round(float(entry.get("pop", 0)) * 100)
                    rain_probability = max(rain_probability, pop_pct)
                    dt_txt = entry.get("dt_txt", "")
                    label = dt_txt[11:16] if len(dt_txt) >= 16 else dt_txt
                    forecast_items.append({
                        "label": label,
                        "temp_c": round(float(entry["main"]["temp"]), 1),
                        "condition": entry["weather"][0]["main"] if entry.get("weather") else "Clear",
                        "rain_prob": pop_pct,
                    })
        except requests.RequestException:
            forecast_items = []

        wind_ms = float(cur.get("wind", {}).get("speed", 0))
        weather_block = (cur.get("weather") or [{}])[0]

        payload = {
            "is_live": True,
            "mode": "live",
            "setup_required": False,
            "status_message": "Live weather data retrieved from OpenWeatherMap.",
            "city": cur.get("name", query_city),
            "country": cur.get("sys", {}).get("country", ""),
            "temperature_c": round(float(cur["main"]["temp"]), 1),
            "feels_like_c": round(float(cur["main"].get("feels_like", cur["main"]["temp"])), 1),
            "humidity": round(float(cur["main"]["humidity"])),
            "condition": weather_block.get("main", "Clear"),
            "description": str(weather_block.get("description", "")).title(),
            "wind_speed_kmh": round(wind_ms * 3.6, 1),
            "rain_probability": rain_probability,
            "forecast": forecast_items,
            "updated_at": datetime.now().strftime("%d %b %Y, %I:%M %p"),
        }
        payload["advisories"] = build_weather_advisories(payload)
        return payload, 200

    except requests.Timeout:
        return {"error": "Weather service request timed out. Please try again."}, 504
    except requests.RequestException:
        return {"error": "Unable to reach weather service right now."}, 502
