def predict_rain_probability(humidity, clouds, wind):
    score = 0.0
    score += humidity / 100 * 0.5
    score += clouds / 100 * 0.3
    score += min(wind / 15, 1) * 0.2
    return round(score, 2)
