import math
from streamlit_js_eval import get_geolocation

# Reference location (Eluru center / your shop location)
SERVICE_LAT = 16.71066
SERVICE_LON = 81.09524

SERVICE_RADIUS_KM = 25  # 20 KM radius service area


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two GPS points in KM
    """

    R = 6371  # Earth radius in KM

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def fetch_user_location():
    """
    Fetch GPS location and check if it is inside service area
    """

    loc = get_geolocation()

    if not loc:
        return None, None, None

    try:

        if "coords" in loc:
            lat = loc["coords"]["latitude"]
            lon = loc["coords"]["longitude"]
        else:
            lat = loc.get("latitude")
            lon = loc.get("longitude")

        if lat and lon:

            distance = haversine_distance(lat, lon, SERVICE_LAT, SERVICE_LON)

            if distance <= SERVICE_RADIUS_KM:
                return lat, lon, True
            else:
                return lat, lon, False

    except Exception:
        pass

    return None, None, None