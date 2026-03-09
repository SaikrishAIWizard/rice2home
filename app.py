import streamlit as st
from src.ui.order_form import show_order_form
from src.config.settings import OWNER_CONTACT, OWNER_NAME

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


st.set_page_config(
    page_title="Rice2Home",
    page_icon="🌾",
    layout="centered"
)

# Load CSS
def load_css():
    with open("styles/main.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ---------- HEADER ----------
col1, col2 = st.columns([1,2])

with col1:
    # Read SVG file content
    # with open("assets/logo.svg") as f:
    #     svg_code = f.read()

    # #st.image("assets/logo3.png", width=160)
    # st.image(svg_code, width=320)
    show_gif("assets/logo.gif", 200)

with col2:
    st.markdown(f"""
    <div class="contact-card">
    <b>Contact</b><br>
    {OWNER_NAME}<br>
    📞 {OWNER_CONTACT}
    </div>
    """, unsafe_allow_html=True)

# ---------- TITLE ----------
st.markdown(
    '<div class="main-title">Rice2Home</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Order premium quality rice bags directly from us</div>',
    unsafe_allow_html=True
)

st.write("")

# ---------- FORM ----------
st.markdown('<div class="form-card">', unsafe_allow_html=True)

show_order_form()

st.markdown('</div>', unsafe_allow_html=True)

from src.config.settings import OWNER_CONTACT

st.markdown(f"""
<a href="https://wa.me/{OWNER_CONTACT}" target="_blank" class="whatsapp-float">

<img src="https://cdn-icons-png.flaticon.com/512/733/733585.png">

</a>
""", unsafe_allow_html=True)