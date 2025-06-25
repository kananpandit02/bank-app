import streamlit as st
from bank_system import BankSystem
from PIL import Image
import time
import plotly.express as px
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Golar Gramin Bank", layout="centered", page_icon="🏦")
bank = BankSystem()

if "user" not in st.session_state:
    st.session_state.user = None

now = datetime.now().strftime("%A %d %B %Y   %H:%M:%S")

# --- Custom Styling & Header ---
st.markdown(f"""
<meta name="viewport" content="width=device-width, initial-scale=1">

<style>
    .header-bar {{
        background-color: #880E4F;
        color: white;
        padding: 8px 16px;
        font-size: 14px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    .header-bar a {{
        color: white;
        margin: 0 10px;
        text-decoration: none;
    }}
    .quote-banner {{
        background-color: #fdd835;
        color: #003566;
        font-weight: 500;
        font-size: 20px;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-top: 10px;
    }}
    .brand-header {{
        background-color: white;
        padding: 20px;
        text-align: center;
    }}
    .brand-header img {{
        width: 80px;
        margin-bottom: 10px;
    }}
    .brand-header h1 {{
        color: #003566;
        font-size: 28px;
        margin-bottom: 4px;
    }}
    .brand-header p {{
        color: #444;
        margin: 0;
    }}
    .custom-footer {{
        position: fixed;
        bottom: 0;
        width: 100%;
        background-color: #f0f0f0;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        color: #444;
        border-top: 1px solid #ccc;
    }}
    .stButton > button {{
        border-radius: 12px;
        font-size: 16px;
        background: linear-gradient(to right, #2c3e50, #3498db);
        color: white;
        padding: 0.6em 1.4em;
        border: none;
    }}
</style>

<div class="header-bar">
  <div>📅 {now}</div>
  <div>
    <a href="#">Notice</a>
    <a href="#">Tenders</a>
    <a href="#">FAQ</a>
    <a href="#">Deposit Rates</a>
    <a href="#">Netbanking</a>
  </div>
</div>

<div class="brand-header">
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Indian_Rupee_symbol.svg/768px-Indian_Rupee_symbol.svg.png" />
    <h1>Golar Gramin Bank</h1>
    <p>💼 A Rural Development Banking Initiative | Sponsored by PNB</p>
</div>

<div class="quote-banner">
    “The ultimate goal of banking is not just saving money, but empowering lives and communities.”
</div>

<div class="custom-footer">
    🛠️ Developed by <strong>Kanan Pandit</strong> — For Software Testing Purposes Only
</div>
""", unsafe_allow_html=True)

# --- Login / Register View ---
def login_section():
    st.markdown("#### 💡 Login or Register Below")
    choice = st.radio("Choose:", ["Login", "Register"], horizonta
