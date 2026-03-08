import streamlit as st
from src.ui.order_form import show_order_form

st.set_page_config(
    page_title="Rice Order Service",
    page_icon="🌾",
    layout="centered"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>

/* Import Premium Font */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap');

html, body, [class*="css"]  {
    font-family: 'Poppins', sans-serif;
}

/* Background */
.stApp{
    background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
}

/* FIX LABEL VISIBILITY */
label, .stTextInput label, .stTextArea label, .stSelectbox label{
    color:white !important;
    font-weight:500;
}

/* Placeholder text */
input::placeholder, textarea::placeholder{
    color:#888 !important;
}

/* Main Container */
.main-container{
    max-width:650px;
    margin:auto;
    padding:40px 20px;
}

/* Logo */
.logo{
    display:flex;
    justify-content:center;
    margin-bottom:15px;
}

/* Title */
.title{
    font-size:42px;
    font-weight:600;
    text-align:center;
    color:white;
    letter-spacing:1px;
}

/* Subtitle */
.subtitle{
    text-align:center;
    font-size:17px;
    color:#e6e6e6;
    margin-bottom:35px;
}

/* Glass Card */
.card{
    background:rgba(255,255,255,0.08);
    backdrop-filter: blur(14px);
    padding:35px;
    border-radius:18px;
    box-shadow:0 20px 40px rgba(0,0,0,0.35);
    border:1px solid rgba(255,255,255,0.15);
}

/* Inputs */
.stTextInput>div>div>input{
    border-radius:10px;
    border:1px solid #dcdcdc;
    padding:10px;
}

.stTextArea textarea{
    border-radius:10px;
    border:1px solid #dcdcdc;
}

/* Dropdown */
.stSelectbox>div>div{
    border-radius:10px;
}

/* Button */
.stButton>button{
    width:100%;
    height:48px;
    border-radius:12px;
    border:none;
    font-size:16px;
    font-weight:600;
    color:white;
    background: linear-gradient(90deg,#00c6ff,#0072ff);
    transition: all 0.3s ease;
}

/* Button Hover */
.stButton>button:hover{
    transform: translateY(-2px);
    box-shadow:0 10px 20px rgba(0,0,0,0.3);
    background: linear-gradient(90deg,#36d1dc,#5b86e5);
}
            
div[data-testid="stMarkdownContainer"] h3 {
        color: white;
    }

</style>
""", unsafe_allow_html=True)
# ---------- MAIN CONTAINER ----------
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# ---------- LOGO ----------
st.markdown('<div class="logo">', unsafe_allow_html=True)
st.image("assets/logo.png", width=120)
st.markdown('</div>', unsafe_allow_html=True)

# ---------- TITLE ----------
st.markdown('<div class="title">Rice Bag Order Service</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="subtitle">Order premium quality rice bags directly from us</div>',
    unsafe_allow_html=True
)

# ---------- FORM CARD ----------
st.markdown('<div class="card">', unsafe_allow_html=True)

show_order_form()

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)