def weather_icon(condition):
    if not condition:
        return "default.png"

    condition = condition.lower()

    if "clear" in condition:
        return "sunny.png"
    if "cloud" in condition:
        return "cloudy.png"
    if "rain" in condition:
        return "rainy.png"
    if "snow" in condition:
        return "snow.png"
    if "storm" in condition or "thunder" in condition:
        return "storm.png"
    if "fog" in condition or "mist" in condition:
        return "fog.png"

    return "default.png"


# ✅ ADD THIS FUNCTION
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
