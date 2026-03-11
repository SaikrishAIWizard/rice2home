import streamlit as st
import folium
from streamlit_folium import st_folium
import time

from src.services.order_service import process_order
from src.config.settings import OWNER_CONTACT, OWNER_NAME
from src.utils.location_service import fetch_user_location
from src.data.rice_companies import rice_companies

import base64


def show_gif(gif_path, width=200):
    with open(gif_path, "rb") as f:
        data = f.read()

    encoded = base64.b64encode(data).decode()

    st.markdown(
        f"""
        <div style="text-align:center;">
            <img src="data:image/gif;base64,{encoded}" width="{width}">
        </div>
        """,
        unsafe_allow_html=True
    )


def show_order_form():

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

    # NEW
    if "order_submitted" not in st.session_state:
        st.session_state.order_submitted = False

    if "gif_stage" not in st.session_state:
        st.session_state.gif_stage = "waiting"

    if "order_data" not in st.session_state:
        st.session_state.order_data = None

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

        lat, lon, availability = fetch_user_location()

        if lat and lon:

            st.session_state.lat = lat
            st.session_state.lon = lon
            st.session_state.gps_location = f"{lat},{lon}"

            st.success("GPS location detected")

            if availability:
                st.success(f"✅ Delivery available in your area Eluru")

            else:
                st.error(f"🚫 Sorry, we are currently serving only in Eluru")
                show_gif("assets/service.gif", 200)
                st.stop()

        else:

            st.markdown(
                """
                <div style="
                    background: rgba(255,255,255,0.08);
                    padding:12px 16px;
                    border-radius:10px;
                    border-left:4px solid #00c6ff;
                    color:white;
                    font-size:15px;
                    margin-top:10px;
                ">
                    📍 Turn on the location and refresh the page...
                </div>
                """,
                unsafe_allow_html=True
            )

    # ---------------------------
    # SHOW MAP
    # ---------------------------

    if st.session_state.lat and st.session_state.lon:

        lat = st.session_state.lat
        lon = st.session_state.lon

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

        name = st.text_input("Name")
        phone = st.text_input("Phone Number")
        address = st.text_area("Address / Landmark")

        st.subheader("Rice Selection")
        company = st.selectbox("Select Rice Company", rice_companies)

        submit_order = st.form_submit_button("Submit Order")

    # ---------------------------
    # PROCESS ORDER
    # ---------------------------

    if submit_order:

        if not st.session_state.gps_location:
            google_link = "NA"

        if not name.strip() or not phone.strip() or not address.strip() or not company.strip():
            st.error("Please fill all details")
            show_gif("assets/waiting.gif", 200)
            st.stop()

        try:
            full_location = f"{address} | GPS:{st.session_state.gps_location}"
            lat, lon = st.session_state.gps_location.split(",")
            google_link = f"https://www.google.com/maps?q={lat},{lon}"
        except:
            full_location = f"{address} | GPS:NA"
            google_link = "NA"

        order_id = process_order(
            name,
            phone,
            full_location,
            company,
            google_link
        )

        # SAVE ORDER DATA
        st.session_state.order_data = {
            "order_id": order_id,
            "name": name,
            "phone": phone,
            "company": company,
            "address": address,
            "google_link": google_link
        }

        st.session_state.order_submitted = True
        st.session_state.gif_stage = "waiting"

    # ---------------------------
    # SHOW SUCCESS SCREEN
    # ---------------------------

    if st.session_state.order_submitted:

        data = st.session_state.order_data

        #st.balloons()

        col1, col2 = st.columns([1, 2])

        with col1:

            gif_placeholder = st.empty()

            if st.session_state.gif_stage == "waiting":
                st.balloons()
                with gif_placeholder:
                    show_gif("assets/orderconfirmed.gif", 200)

                time.sleep(12)

                st.session_state.gif_stage = "done"
                st.rerun()

            elif st.session_state.gif_stage == "done":

                with gif_placeholder:
                    show_gif("assets/happy_delivery.gif", 200)

        with col2:

            st.success("✅ Order Submitted Successfully!")

            st.markdown(
                                    f"""
                    ### 📦 Order Details

                    **Order ID:** {data['order_id']}  
                    **Customer:** {data['name']}  
                    **Phone:** {data['phone']}  
                    **Rice Brand:** {data['company']}

                    📍 **Delivery Location**  
                    {data['address']}

                    [Open in Google Maps]({data['google_link']})

                    ---

                    🚚 Our team will contact you shortly.

                    **Contact**  
                    {OWNER_NAME}  
                    📞 {OWNER_CONTACT}
                    """
                                )

    else:
        show_gif("assets/checkalldetails.gif", 200)