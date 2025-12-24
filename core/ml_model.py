def predict_temperature(weather_data):
    """
    Dummy ML prediction for now.
    This avoids circular imports and lets the server start.
    """
    return weather_data.get("temperature", 0)

def predict_temperature(temp, humidity, wind):
    return round(temp + (humidity * 0.01) - (wind * 0.2), 2)

