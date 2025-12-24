import requests
from core.utils import weather_icon

OPENWEATHER_API_KEY = "c39c6cd254f22917bef01808c3ff76d9"  # 🔥 double-check this

BASE_URL = "https://api.openweathermap.org/data/2.5"


def get_current_weather(city):
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"
        }

        res = requests.get(url, params=params, timeout=10)

        print("STATUS:", res.status_code)
        print("RESPONSE:", res.text)

        if res.status_code != 200:
            return None

        data = res.json()

        return {
            "city": data["name"],
            "temperature": round(data["main"]["temp"], 1),
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"].title(),
            "icon": weather_icon(data["weather"][0]["description"]),
        }

    except Exception as e:
        print("ERROR:", e)
        return None



def get_forecast_by_city(city):
    try:
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

        for item in data["list"][:8]:  # next 24 hrs (3h interval)
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


def get_weekly_forecast(city):
    # Mock 7-day data (OpenWeather free plan limitation)
    return {
        "labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "temps": [29, 30, 31, 30, 29, 28, 27],
    }


def get_ai_prediction():
    # Mock AI prediction (replace later with ML model)
    return {
        "labels": ["+1h", "+2h", "+3h", "+4h", "+5h"],
        "temps": [30, 31, 31.5, 32, 32.2],
    }
