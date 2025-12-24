from django.urls import path
from . import views

urlpatterns = [
    path("weather/current/", views.current_weather, name="current_weather"),
    path("weather/predict/", views.predict_weather, name="predict_weather"),
]
