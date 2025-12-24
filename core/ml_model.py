# core/ml_model.py

def predict_temperature(weather_data: dict) -> float:
    """
    Dummy ML prediction for now.
    This keeps Render deployment fast and stable.
    You can replace logic later with real ML.
    """
    try:
        temp = weather_data.get("temperature", 25)
        humidity = weather_data.get("humidity", 60)

        # Simple heuristic (placeholder ML)
        predicted = temp + (humidity * 0.02)
        return round(predicted, 2)

    except Exception:
        return 25.0
