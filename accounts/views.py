import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from core.services import (
    get_current_weather,
    get_forecast_by_city,
    get_weekly_forecast,
    get_ai_prediction,
)

from core.utils import weather_icon, get_bg_class



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
# LOGIN
# =========================
def login_view(request):
    return render(request, "accounts/login.html")


    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(
                request,
                username=user_obj.username,
                password=password
            )
        except User.DoesNotExist:
            user = None

        if user:
            login(request, user)
            return redirect("dashboard")
        else:
            error = "Invalid email or password"

    return render(request, "accounts/login.html", {"error": error})


# =========================
# REGISTER
# =========================
def register_view(request):
    error = None

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")

        if password != confirm:
            error = "Passwords do not match"
        elif User.objects.filter(username=email).exists():
            error = "User already exists"
        else:
            User.objects.create_user(
                username=email,
                email=email,
                password=password
            )
            return redirect("login")

    return render(request, "accounts/register.html", {"error": error})


# =========================
# DASHBOARD
# =========================
@login_required
def dashboard_view(request):
    # -------------------------
    # City input
    # -------------------------
    city = request.GET.get("city", "Chennai")

    # -------------------------
    # API Calls
    # -------------------------
    weather = get_current_weather(city)
    forecast = get_forecast_by_city(city)

    # -------------------------
    # Background + Icon
    # -------------------------
    bg_class = "bg-default"
    icon = None

    if weather and weather.get("description"):
        bg_class = get_bg_class(weather["description"])
        icon = weather_icon(weather["description"])

    # -------------------------
    # Hourly Chart Data
    # -------------------------
    chart_data = None
    if forecast and "chart" in forecast:
        chart_data = {
            "labels": json.dumps(forecast["chart"]["labels"]),
            "temps": json.dumps(forecast["chart"]["temps"]),
            "humidity": json.dumps(forecast["chart"]["humidity"]),
        }

    # -------------------------
    # Weekly Forecast Chart
    # -------------------------
    weekly_chart = None
    weekly = get_weekly_forecast(city)

    if weekly:
        weekly_chart = {
            "labels": json.dumps(weekly["labels"]),
            "temps": json.dumps(weekly["temps"]),
        }

    # -------------------------
    # AI Prediction (Mock / ML Ready)
    # -------------------------
    ai_prediction = None
    ai = get_ai_prediction()

    if ai:
        ai_prediction = {
            "labels": json.dumps(ai["labels"]),
            "temps": json.dumps(ai["temps"]),
        }

    # -------------------------
    # Render Dashboard
    # -------------------------
    return render(request, "accounts/dashboard.html", {
        "city": city,
        "weather": weather,
        "forecast": forecast,
        "icon": icon,
        "bg_class": bg_class,          # 👈 dynamic background
        "chart_data": chart_data,
        "weekly_chart": weekly_chart,
        "ai_prediction": ai_prediction,
    })
# =========================
# LOGOUT
# =========================
def logout_view(request):
    logout(request)
    return redirect("login")
