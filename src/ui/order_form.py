import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation

from src.services.order_service import process_order
from src.data.rice_companies import rice_companies
from src.config.settings import OWNER_CONTACT, OWNER_NAME


def show_order_form():

    st.subheader("Customer Details")

    name = st.text_input("Customer Name")
    phone = st.text_input("Phone Number")
    location = st.text_area("Address / Landmark")

    # -------------------------------
    # SESSION STATE INITIALIZATION
    # -------------------------------

    if "show_map" not in st.session_state:
        st.session_state.show_map = False

    if "lat" not in st.session_state:
        st.session_state.lat = None

    if "lon" not in st.session_state:
        st.session_state.lon = None

    if "gps_location" not in st.session_state:
        st.session_state.gps_location = ""

    st.subheader("📍 Delivery Location")

    # -------------------------------
    # GET CURRENT GPS LOCATION
    # -------------------------------

    if st.button("Get My Current Location 📍"):

        loc = get_geolocation()

        if loc is not None:

            st.session_state.lat = loc["coords"]["latitude"]
            st.session_state.lon = loc["coords"]["longitude"]
            st.session_state.show_map = True

            st.success("GPS location detected successfully")

        else:

            st.warning("⚠ Could not detect GPS automatically")

            # fallback location (India center)
            st.session_state.lat = 20.5937
            st.session_state.lon = 78.9629
            st.session_state.show_map = True

            st.info("Please select your location manually on the map")

    # -------------------------------
    # SHOW MAP
    # -------------------------------

    if st.session_state.show_map:

        lat = st.session_state.lat
        lon = st.session_state.lon

        st.info("Click on the map to confirm your exact delivery location")

        m = folium.Map(
            location=[lat, lon],
            zoom_start=18,
            control_scale=True
        )

        # Marker for detected GPS location
        folium.Marker(
            [lat, lon],
            tooltip="Detected GPS Location",
            icon=folium.Icon(color="green", icon="home")
        ).add_to(m)

        map_data = st_folium(m, height=450, width=700)

        # -------------------------------
        # USER CLICK LOCATION
        # -------------------------------

        if map_data and map_data.get("last_clicked"):

            clicked_lat = map_data["last_clicked"]["lat"]
            clicked_lon = map_data["last_clicked"]["lng"]

            st.session_state.gps_location = f"{clicked_lat},{clicked_lon}"

            st.success(f"Selected Location: {clicked_lat}, {clicked_lon}")

            google_map_link = f"https://www.google.com/maps?q={clicked_lat},{clicked_lon}"

            st.markdown(f"📍 **Google Maps:** [Open Location]({google_map_link})")

    # -------------------------------
    # RICE COMPANY SELECTION
    # -------------------------------

    st.subheader("Rice Selection")

    company_options = ["Other (Enter Manually)"] + rice_companies

    company = st.selectbox(
        "Select Rice Company",
        company_options
    )

    if company == "Other (Enter Manually)":
        company = st.text_input("Enter Rice Bag Company Name")

    # -------------------------------
    # SUBMIT ORDER
    # -------------------------------

    if st.button("Submit Order"):

        if name and phone and location and company:

            full_location = f"{location} | GPS: {st.session_state.gps_location}"

            order_id = process_order(
                name,
                phone,
                full_location,
                company
            )

            st.success("✅ Order Submitted Successfully")

            st.info(f"""
Reference Order Number: **{order_id}**

Our team will contact you shortly.

Contact Details  
{OWNER_NAME}  
📞 {OWNER_CONTACT}
""")

        else:

            st.error("Please fill all required details")