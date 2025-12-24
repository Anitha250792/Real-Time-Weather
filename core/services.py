import os
import requests
from core.utils import weather_icon

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5"


def get_current_weather(city: str):
    try:
        if not OPENWEATHER_API_KEY:
            raise Exception("Missing OpenWeather API key")

        url = f"{BASE_URL}/weather"
        params = {
            "q": city,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric",
        }

        res = requests.get(url, params=params, timeout=10)
        print("STATUS:", res.status_code)
        print("RAW:", res.text)

        res.raise_for_status()
        data = res.json()

        weather_desc = data.get("weather", [{}])[0].get("description", "clear")

        return {
            "city": data.get("name", city),
            "temperature": round(data.get("main", {}).get("temp", 0), 1),
            "humidity": data.get("main", {}).get("humidity", 0),
            "description": weather_desc.title(),
            "icon": weather_icon(weather_desc),
        }

    except Exception as e:
        print("Weather Error:", e)
        return None



def get_forecast_by_city(city: str):
    try:
        if not OPENWEATHER_API_KEY:
            raise Exception("Missing OpenWeather API key")

        url = f"{BASE_URL}/forecast"
        params = {
            "q": city,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric",
        }

        res = requests.get(url, params=params, timeout=10)

        if res.status_code != 200:
            return None

        data = res.json()

        labels, temps, humidity, hourly = [], [], [], []

        for item in data["list"][:8]:  # 24 hours (3h interval)
            labels.append(item["dt_txt"][11:16])
            temps.append(round(item["main"]["temp"], 1))
            humidity.append(item["main"]["humidity"])

            hourly.append({
                "time": item["dt_txt"],
                "temp": round(item["main"]["temp"], 1),
                "icon": weather_icon(item["weather"][0]["description"]),
            })

        return {
            "hourly": hourly,
            "chart": {
                "labels": labels,
                "temps": temps,
                "humidity": humidity,
            },
        }

    except Exception as e:
        print("Forecast Error:", e)
        return None


def get_weekly_forecast(city: str):
    # Mock 7-day data (free API limitation)
    return {
        "labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "temps": [29, 30, 31, 30, 29, 28, 27],
    }


def get_ai_prediction():
    # Mock AI output (replace with ML later)
    return {
        "labels": ["+1h", "+2h", "+3h", "+4h", "+5h"],
        "temps": [30, 31, 31.5, 32, 32.2],
    }
