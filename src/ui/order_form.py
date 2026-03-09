import streamlit as st
import folium
from streamlit_folium import st_folium

from src.services.order_service import process_order
from src.config.settings import OWNER_CONTACT, OWNER_NAME
from src.utils.location_service import fetch_user_location
from src.data.rice_companies import rice_companies


def show_order_form():

    #st.title("🛒 Rice Bags ")

    # ---------------------------
    # SESSION STATE
    # ---------------------------

    if "lat" not in st.session_state:
        st.session_state.lat = None

    if "lon" not in st.session_state:
        st.session_state.lon = None

    if "gps_location" not in st.session_state:
        st.session_state.gps_location = None

    if "get_location_trigger" not in st.session_state:
        st.session_state.get_location_trigger = False

    # ---------------------------
    # GPS BUTTON
    # ---------------------------

    st.subheader("📍 Delivery Location")

    if st.button("Get My Current Location 📍"):
        st.session_state.get_location_trigger = True

    # ---------------------------
    # GET LOCATION FROM SERVICE
    # ---------------------------

    if st.session_state.get_location_trigger:

        lat, lon = fetch_user_location()

        if lat and lon:

            st.session_state.lat = lat
            st.session_state.lon = lon

            st.session_state.gps_location = f"{lat},{lon}"

            st.success("GPS location detected")

        else:

            st.info("Turn on the GPS and double click on the 📍...")

    # ---------------------------
    # SHOW MAP
    # ---------------------------

    if st.session_state.lat and st.session_state.lon:

        lat = st.session_state.lat
        lon = st.session_state.lon

        st.info("Click map to adjust delivery location")

        m = folium.Map(
            location=[lat, lon],
            zoom_start=18
        )

        folium.Marker(
            [lat, lon],
            tooltip="Current Location",
            icon=folium.Icon(color="red", icon="home")
        ).add_to(m)

        map_data = st_folium(
            m,
            height=400,
            width=700
        )

        if map_data and map_data.get("last_clicked"):

            clicked_lat = map_data["last_clicked"]["lat"]
            clicked_lon = map_data["last_clicked"]["lng"]

            st.session_state.gps_location = f"{clicked_lat},{clicked_lon}"

    # ---------------------------
    # SHOW SELECTED LOCATION
    # ---------------------------

    if st.session_state.gps_location:

        lat, lon = st.session_state.gps_location.split(",")

        st.success(f"📍 Selected Location: {lat}, {lon}")

        google_link = f"https://www.google.com/maps?q={lat},{lon}"

        st.markdown(f"[Open in Google Maps]({google_link})")

    # ---------------------------
    # ORDER FORM
    # ---------------------------

    with st.form("order_form"):

        st.subheader("Customer Details")

        name = st.text_input("Customer Name")
        phone = st.text_input("Phone Number")
        address = st.text_area("Address / Landmark")

        # st.subheader("Rice Selection")

        # company = st.text_input("Enter Rice Company Name")
        st.subheader("Rice Selection")
        company = st.selectbox(
                 "Select Rice Company", rice_companies)

        submit_order = st.form_submit_button("Submit Order")

    # ---------------------------
    # PROCESS ORDER
    # ---------------------------

    if submit_order:

        if not st.session_state.gps_location:
            st.error("Please select delivery location")
            return

        if not name.strip() or not phone.strip() or not address.strip() or not company.strip():
            st.error("Please fill all details")
            return

        full_location = f"{address} | GPS:{st.session_state.gps_location}"

        order_id = process_order(
            name,
            phone,
            full_location,
            company,
            google_link
        )

        st.success("✅ Order Submitted Successfully")

        st.info(f"""
Reference Order Number: **{order_id}**

Our team will contact you shortly.

Contact  
{OWNER_NAME}  
📞 {OWNER_CONTACT}
""")