import streamlit as st
from src.config.settings import OWNER_NAME, OWNER_CONTACT


def show_header():

    st.markdown(
        f"""
        <div class="header">
            <div class="logo">
                <img src="app/static/assets/logo2.png">
            </div>

            <div class="contact-box">
                <strong>Contact</strong><br>
                {OWNER_NAME}<br>
                📞 {OWNER_CONTACT}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )