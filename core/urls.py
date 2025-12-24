from django.urls import path
from . import views
from .ml_model import predict_temperature


urlpatterns = [
    path('weather/current/', views.current_weather, name='current_weather'),
    path('weather/predict/', views.predict_weather, name='predict_weather'),
]
