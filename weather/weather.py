#!/usr/bin/env python3
"""Generate a simple live weather JSON feed for ZevTV.

Uses Open-Meteo's public forecast API. No API key is required.
The generated weather.json can be consumed by a renderer or web player.
"""
import json, time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parent
CONFIG = ROOT / "locations.json"
OUT = ROOT / "output" / "weather.json"

WMO = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Rime fog", 51: "Light drizzle", 53: "Drizzle",
    55: "Heavy drizzle", 61: "Light rain", 63: "Rain", 65: "Heavy rain",
    71: "Light snow", 73: "Snow", 75: "Heavy snow", 80: "Rain showers",
    81: "Rain showers", 82: "Heavy rain showers", 95: "Thunderstorm",
    96: "Thunderstorm with hail", 99: "Thunderstorm with hail"
}

def fetch(location):
    params = {
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,sunrise,sunset",
        "timezone": "auto",
        "forecast_days": 7
    }
    url = "https://api.open-meteo.com/v1/forecast?" + urlencode(params)
    with urlopen(url, timeout=15) as response:
        return json.load(response)

def main():
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    locations = []
    for location in config["locations"]:
        data = fetch(location)
        current = data["current"]
        daily = data["daily"]
        locations.append({
            "name": location["name"],
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "updated": datetime.now(timezone.utc).isoformat(),
            "current": {
                "temperature_c": current["temperature_2m"],
                "feels_like_c": current["apparent_temperature"],
                "humidity_percent": current["relative_humidity_2m"],
                "wind_kmh": current["wind_speed_10m"],
                "condition": WMO.get(current["weather_code"], "Unknown")
            },
            "forecast": [
                {
                    "date": daily["time"][i],
                    "condition": WMO.get(daily["weather_code"][i], "Unknown"),
                    "high_c": daily["temperature_2m_max"][i],
                    "low_c": daily["temperature_2m_min"][i],
                    "rain_chance_percent": daily["precipitation_probability_max"][i],
                    "sunrise": daily["sunrise"][i],
                    "sunset": daily["sunset"][i]
                }
                for i in range(len(daily["time"]))
            ]
        })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "channel": "ZevTV Weather",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "locations": locations
    }, indent=2), encoding="utf-8")
    print(f"Generated {OUT}")

if __name__ == "__main__":
    main()
