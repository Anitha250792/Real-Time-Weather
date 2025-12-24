from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .services import get_current_weather
from .ml_model import predict_temperature


@require_GET
def current_weather(request):
    city = request.GET.get("city", "Chennai")

    weather = get_current_weather(city)
    if not weather:
        return JsonResponse({"error": "Could not fetch weather"}, status=500)

    return JsonResponse(weather)


@require_GET
def predict_weather(request):
    city = request.GET.get("city", "Chennai")

    weather = get_current_weather(city)
    if not weather:
        return JsonResponse({"error": "Could not fetch weather"}, status=500)

    predicted_temp = predict_temperature(weather)

    return JsonResponse({
        "city": weather["city"],
        "current_temperature": weather["temperature"],
        "predicted_temperature_next": round(predicted_temp, 2),
        "humidity": weather["humidity"],
        "pressure": weather["pressure"],
        "wind_speed": weather["wind_speed"],
        "clouds": weather["clouds"],
    })
