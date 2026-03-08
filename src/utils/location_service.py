from streamlit_js_eval import get_geolocation


def fetch_user_location():
    """
    Safely fetch user GPS location from browser.
    Handles different response formats.
    """

    loc = get_geolocation()

    if not loc:
        return None, None

    try:

        # Format 1: {"coords": {"latitude": .., "longitude": ..}}
        if "coords" in loc:
            lat = loc["coords"]["latitude"]
            lon = loc["coords"]["longitude"]

        # Format 2: {"latitude": .., "longitude": ..}
        else:
            lat = loc.get("latitude")
            lon = loc.get("longitude")

        if lat and lon:
            return lat, lon

    except Exception:
        pass

    return None, None