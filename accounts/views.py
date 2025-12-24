import json
from django.shortcuts import render

from core.services import (
    get_current_weather,
    get_forecast_by_city,
    get_weekly_forecast,
    get_ai_prediction,
)
from core.utils import weather_icon


# =========================
# Weather → Background Map
# =========================
def get_bg_class(description):
    if not description:
        return "bg-default"

    desc = description.lower()

    if "rain" in desc:
        return "bg-rain"
    if "cloud" in desc:
        return "bg-cloudy"
    if "clear" in desc:
        return "bg-clear"
    if "fog" in desc or "mist" in desc:
        return "bg-fog"
    if "snow" in desc:
        return "bg-snow"

    return "bg-default"


# =========================
# DASHBOARD (PUBLIC)
# =========================
def dashboard_view(request):
    city = request.GET.get("city", "Chennai")

    # API calls
    weather = get_current_weather(city)
    forecast = get_forecast_by_city(city)

    # Background & icon
    bg_class = "bg-default"
    icon = None

    if weather and weather.get("description"):
        bg_class = get_bg_class(weather["description"])
        icon = weather_icon(weather["description"])

    # Hourly chart
    chart_data = None
    if forecast and "chart" in forecast:
        chart_data = {
            "labels": json.dumps(forecast["chart"]["labels"]),
            "temps": json.dumps(forecast["chart"]["temps"]),
            "humidity": json.dumps(forecast["chart"]["humidity"]),
        }

    # Weekly forecast
    weekly_chart = None
    weekly = get_weekly_forecast(city)
    if weekly:
        weekly_chart = {
            "labels": json.dumps(weekly["labels"]),
            "temps": json.dumps(weekly["temps"]),
        }

    # AI prediction
    ai_prediction = None
    ai = get_ai_prediction()
    if ai:
        ai_prediction = {
            "labels": json.dumps(ai["labels"]),
            "temps": json.dumps(ai["temps"]),
        }

    return render(request, "accounts/dashboard.html", {
        "city": city,
        "weather": weather,
        "forecast": forecast,
        "icon": icon,
        "bg_class": bg_class,
        "chart_data": chart_data,
        "weekly_chart": weekly_chart,
        "ai_prediction": ai_prediction,
        "error": None if weather else "City not found",
    })
