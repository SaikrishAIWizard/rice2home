import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation

from src.services.order_service import process_order
from src.data.rice_companies import rice_companies
from src.config.settings import OWNER_CONTACT, OWNER_NAME


def show_order_form():

    st.title("🛒 Rice Bag Order")

    # ---------------------------
    # SESSION STATE
    # ---------------------------

    if "lat" not in st.session_state:
        st.session_state.lat = None

    if "lon" not in st.session_state:
        st.session_state.lon = None

    if "gps_location" not in st.session_state:
        st.session_state.gps_location = None

    if "gps_requested" not in st.session_state:
        st.session_state.gps_requested = False

    # ---------------------------
    # CUSTOMER FORM
    # ---------------------------

    with st.form("order_form"):

        st.subheader("Customer Details")

        name = st.text_input("Customer Name")
        phone = st.text_input("Phone Number")
        address = st.text_area("Address / Landmark")

        # ---------------------------
        # LOCATION
        # ---------------------------

        st.subheader("📍 Delivery Location")

        get_location = st.form_submit_button("Get My Current Location 📍")

        if get_location:
            st.session_state.gps_requested = True

        # ---------------------------
        # GPS DETECTION
        # ---------------------------

        if st.session_state.gps_requested:

            loc = get_geolocation()

            if loc:

                st.session_state.lat = loc["coords"]["latitude"]
                st.session_state.lon = loc["coords"]["longitude"]

                # auto save GPS
                st.session_state.gps_location = f"{st.session_state.lat},{st.session_state.lon}"

                st.success("GPS location detected")

            else:
                st.info("Waiting for browser location permission...")

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

            # marker
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
        # RICE COMPANY
        # ---------------------------

        st.subheader("Rice Selection")

        company_options = ["Other (Enter Manually)"] + rice_companies

        # selected_company = st.selectbox(
        #     "Select Rice Company",
        #     company_options
        # )

        #if selected_company == "Other (Enter Manually)":
        company = st.text_input("Enter Rice Company Name")
        #else:
        #    company = selected_company

        # ---------------------------
        # SUBMIT ORDER
        # ---------------------------

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