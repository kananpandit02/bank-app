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
    }}
    .stButton > button {{
        border-radius: 12px;
        font-size: 16px;
        background: linear-gradient(to right, #2c3e50, #3498db);
        color: white;
        padding: 0.6em 1.4em;
        border: none;
    }}
    .fixed-dashboard-btn {{
        position: fixed;
        top: 80px;
        left: 10px;
        background: #0072ff;
        color: white;
        padding: 10px 16px;
        font-size: 16px;
        font-weight: bold;
        border-radius: 8px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
        z-index: 9999;
        transition: all 0.3s ease-in-out;
    }}
    .fixed-dashboard-btn:hover {{
        background: #005bb5;
        cursor: pointer;
    }}
</style>
<div class="header-bar">
  <div>🗕️ {now}</div>
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
<a href="#dashboard" class="fixed-dashboard-btn">🏠 Dashboard</a>
""", unsafe_allow_html=True)

# --- Login / Register View ---
def login_section():
    st.markdown("#### 💡 Login or Register Below")
    choice = st.radio("Choose:", ["Login", "Register"], horizontal=True)
    st.write("---")

    name = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")

    if st.button("Submit"):
        if not name or not password:
            st.warning("⚠️ Please enter both username and password.")
            return

        try:
            password = int(password)
        except ValueError:
            st.error("🛑 Password must be numeric.")
            return

        if choice == "Login":
            if bank.login(name, password):
                st.session_state.user = name
                st.success(f"✅ Welcome back, {name.capitalize()}!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Invalid credentials.")
        else:
            if bank.user_exists(name):
                st.warning("⚠️ User already exists. Try logging in.")
            else:
                bank.register(name, password)
                st.success("✅ Registration successful! Please login now.")

# --- Dashboard View ---
def dashboard():
    st.sidebar.markdown(f"### 👤 {st.session_state.user.capitalize()}")
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    menu = st.sidebar.radio("📋 Menu", ["🏦 Dashboard", "➕ Deposit", "➖ Withdraw", "🔁 Transfer", "📜 History", "📈 Analytics", "🚪 Logout"])

    if menu == "🏦 Dashboard":
        st.markdown('<div id="dashboard"></div>', unsafe_allow_html=True)
        st.title("💳 Account Overview")
        balance = bank.get_balance(st.session_state.user)
        st.metric("Available Balance", f"₹{balance}")
        st.balloons()

    if menu == "➕ Deposit":
        st.subheader("➕ Deposit Money")
        amount = st.number_input("Enter amount", min_value=1)
        if st.button("Deposit"):
            bank.deposit(st.session_state.user, amount)
            st.success(f"✅ ₹{amount} deposited successfully!")

    if menu == "➖ Withdraw":
        st.subheader("➖ Withdraw Money")
        amount = st.number_input("Enter amount", min_value=1)
        if st.button("Withdraw"):
            if bank.withdraw(st.session_state.user, amount):
                st.success(f"✅ ₹{amount} withdrawn successfully!")
            else:
                st.error("❌ Not enough balance.")

    if menu == "🔁 Transfer":
        st.subheader("🔁 Transfer Funds")
        recipient = st.text_input("👤 Recipient Name")
        amount = st.number_input("Enter amount", min_value=1)
        if st.button("Transfer"):
            if recipient == st.session_state.user:
                st.warning("⚠️ You cannot transfer to yourself.")
            else:
                if bank.transfer(st.session_state.user, recipient, amount):
                    st.success(f"✅ ₹{amount} sent to {recipient}")
                else:
                    st.error("❌ Transfer failed. Check balance or username.")

    if menu == "📜 History":
        st.subheader("📜 Transaction History")
        history = bank.get_history(st.session_state.user)
        if history:
            for txn in reversed(history[-10:]):
                st.info(txn)
        else:
            st.write("No transactions yet.")

    if menu == "📈 Analytics":
        st.subheader("📈 Transaction Summary")
        history = bank.get_history(st.session_state.user)
        if not history:
            st.info("No transactions yet.")
        else:
            txn_counts = {"Deposit": 0, "Withdraw": 0, "Transfer": 0}
            for line in history:
                for key in txn_counts:
                    if key.lower() in line.lower():
                        txn_counts[key] += 1
            df = pd.DataFrame({
                "Transaction Type": list(txn_counts.keys()),
                "Count": list(txn_counts.values())
            })
            fig = px.bar(df, x="Transaction Type", y="Count",
                         title="Transaction Distribution",
                         color="Transaction Type",
                         color_discrete_sequence=px.colors.qualitative.Set2)
            st.plotly_chart(fig)

    if menu == "🚪 Logout":
        st.session_state.user = None
        st.success("✅ Logged out.")
        time.sleep(1)
        st.rerun()

# Render based on login status
if st.session_state.user:
    dashboard()
else:
    login_section()

# Footer with credit
st.markdown("""
<div class="custom-footer">
    ✨ Developed by <strong>Kanan Pandit</strong> | For software testing & educational purposes only.
</div>
""", unsafe_allow_html=True)
