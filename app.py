import streamlit as st
from bank_system import BankSystem
from PIL import Image
import time
import plotly.express as px
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Golar Gramin Bank", layout="wide", page_icon="🏦")
bank = BankSystem()

if "user" not in st.session_state:
    st.session_state.user = None
if "acc_no" not in st.session_state:
    st.session_state.acc_no = None

now = datetime.now().strftime("%A, %d %B %Y | %I:%M:%S %p")

# --- Custom Styling & Header ---
nav_links = """
<a href="#">Home</a>
<a href="#">Schemes</a>
<a href="#">Deposits</a>
<a href="#">Netbanking</a>
<a href="#">FAQ</a>
"""
if st.session_state.user:
    nav_links += '<a href="#dashboard">Dashboard</a>'

st.markdown(f"""
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
    .nav-bar {{
        background-color: #003566;
        padding: 10px 20px;
        color: white;
        font-size: 18px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    .nav-links a {{
        color: white;
        text-decoration: none;
        margin: 0 10px;
    }}
    .nav-links a:hover {{
        color: #ffd60a;
    }}
    .quote-banner {{
        background-color: #ffd60a;
        color: #003566;
        font-weight: 500;
        font-size: 20px;
        padding: 15px;
        text-align: center;
        margin: 10px 0;
        border-radius: 12px;
    }}
    .footer {{
        margin-top: 20px;
        font-size: 14px;
        color: #888;
        text-align: center;
    }}
    .stButton > button {{
        border-radius: 10px;
        font-size: 16px;
        background-color: #003566;
        color: white;
        padding: 8px 16px;
    }}
</style>
<div class="nav-bar">
  <div><strong>🌐 Golar Gramin Bank</strong></div>
  <div class="nav-links">
    {nav_links}
  </div>
  <div>🕒 {now}</div>
</div>
<div class="quote-banner">
    "The ultimate goal of banking is not just saving money, but empowering lives and communities."
</div>
""", unsafe_allow_html=True)

# --- Login/Register Section ---
def login_section():
    st.markdown("#### 💡 Login or Register")
    choice = st.radio("Select Option", ["Login", "Register"], horizontal=True)
    st.write("---")

    if choice == "Register":
        acc_no = st.text_input("🌐 Account Number (10 digits)")
        name = st.text_input("👤 Full Name")
        password = st.text_input("🔑 Password", type="password")

        if st.button("Register"):
            if len(acc_no) != 10 or not acc_no.isdigit():
                st.error("Account number must be 10 digits.")
            else:
                success, msg = bank.register(acc_no, name, password)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)

    else:
        identifier = st.text_input("📄 Account No / Username")
        password = st.text_input("🔑 Password", type="password")

        if st.button("Login"):
            acc_no = bank.login(identifier, password)
            if acc_no:
                st.session_state.user = bank.users[acc_no]["name"]
                st.session_state.acc_no = acc_no
                st.success(f"✅ Welcome {st.session_state.user}!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Invalid credentials")

# --- Dashboard ---
def dashboard():
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
    st.sidebar.markdown(f"### 👤 {st.session_state.user}")
    menu = st.sidebar.radio("Menu", ["Dashboard", "Deposit", "Withdraw", "Transfer", "History", "Analytics", "Logout"])

    acc_no = st.session_state.acc_no

    st.markdown('<div id="dashboard"></div>', unsafe_allow_html=True)

    if menu == "Dashboard":
        st.title("💼 Account Dashboard")
        balance = bank.get_balance(acc_no)
        st.metric("Available Balance", f"₹{balance}")

    elif menu == "Deposit":
        st.subheader("Deposit Money")
        amt = st.number_input("Enter amount", min_value=1)
        if st.button("Deposit"):
            bank.deposit(acc_no, amt)
            st.success(f"✅ Deposited ₹{amt}")

    elif menu == "Withdraw":
        st.subheader("Withdraw Money")
        amt = st.number_input("Enter amount", min_value=1)
        if st.button("Withdraw"):
            if bank.withdraw(acc_no, amt):
                st.success(f"✅ Withdrew ₹{amt}")
            else:
                st.error("❌ Insufficient balance")

    elif menu == "Transfer":
        st.subheader("Transfer Money")
        recipient = st.text_input("Recipient Username")
        amt = st.number_input("Enter amount", min_value=1)
        if st.button("Transfer"):
            if recipient == st.session_state.user:
                st.warning("You cannot transfer to yourself")
            elif bank.transfer(acc_no, recipient, amt):
                st.success(f"✅ Transferred ₹{amt} to {recipient}")
            else:
                st.error("Transfer failed")

    elif menu == "History":
        st.subheader("Transaction History")
        history = bank.get_history(acc_no)
        if history:
            for h in reversed(history[-10:]):
                st.info(h)
        else:
            st.write("No transaction history yet")

    elif menu == "Analytics":
        st.subheader("Transaction Analytics")
        history = bank.get_history(acc_no)
        if not history:
            st.info("No data")
        else:
            txn_type = {"Deposit": 0, "Withdraw": 0, "Transfer": 0}
            for h in history:
                for key in txn_type:
                    if key.lower() in h.lower():
                        txn_type[key] += 1
            df = pd.DataFrame({"Transaction": txn_type.keys(), "Count": txn_type.values()})
            fig = px.pie(df, names="Transaction", values="Count", title="Your Transactions")
            st.plotly_chart(fig)

    elif menu == "Logout":
        st.session_state.user = None
        st.session_state.acc_no = None
        st.success("Logged out")
        time.sleep(1)
        st.rerun()

# --- Main Flow ---
if st.session_state.user:
    dashboard()
else:
    login_section()

# --- Footer ---
st.markdown("""
<div class="footer" style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center; font-size: 14px; color: #333;">
    <strong>Developed & Maintained by <span style="color:#003566;">Kanan Pandit</span></strong> — <strong><span style="color:black;">Aspiring Data Scientist</span></strong><br>
    🎓 <strong>M.Sc. in Big Data Analytics</strong>, RKMVERI, Belur Math<br>
    📧 <strong><a href="mailto:kananpandit02@gmail.com" target="_blank">kananpandit02@gmail.com</a></strong> |
    💼 <strong><a href="https://linkedin.com/in/kananpandit02" target="_blank">LinkedIn</a></strong> |
    🧠 <strong><a href="https://github.com/kananpandit02" target="_blank">GitHub</a></strong> |
    🌐 <strong><a href="https://kananpanditportfolio.netlify.app/" target="_blank">Portfolio</a></strong>
    <br><br>
    <em><strong>"Empowering Digital Banking through Data & Design"</strong></em>
</div>
""", unsafe_allow_html=True)
