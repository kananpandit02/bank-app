import streamlit as st
from bank_system import BankSystem
from PIL import Image
import time
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Golar Gramin Bank", layout="centered", page_icon="🏦")
bank = BankSystem()

# Session state init
if "user" not in st.session_state:
    st.session_state.user = None
if "just_logged_in" not in st.session_state:
    st.session_state.just_logged_in = False

# UI Styling
st.markdown("""
    <style>
        body {
            background: linear-gradient(to right, #dbe6f6, #c5796d);
        }
        .main-title {
            text-align: center;
            font-size: 44px;
            font-weight: bold;
            color: #003566;
            animation: fadeIn 1s ease-in-out;
        }
        .stButton > button {
            border-radius: 12px;
            font-size: 16px;
            background: linear-gradient(to right, #2c3e50, #3498db);
            color: white;
            padding: 0.6em 1.4em;
            border: none;
            transition: 0.3s ease;
        }
        .stButton > button:hover {
            background: linear-gradient(to right, #3498db, #2c3e50);
        }
        .stRadio > div {
            flex-direction: row !important;
            justify-content: center;
        }
        .custom-footer {
            position: fixed;
            bottom: 0;
            width: 100%;
            background-color: #f0f0f0;
            text-align: center;
            padding: 10px;
            font-size: 14px;
            color: #444;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
    <div class="custom-footer">
        🏦 <strong>Golar Gramin Bank</strong> | 💻 Developed by <strong>Kanan Pandit</strong> | 🔐 Secure Banking Portal
    </div>
""", unsafe_allow_html=True)

# --- LOGIN / REGISTER ---
def login_section():
    st.markdown("<h1 class='main-title'>🔐 Welcome to Golar Gramin Bank</h1>", unsafe_allow_html=True)
    st.markdown("#### 💡 Banking for Every Village, with Trust and Technology")
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
            st.error("🚫 Password must be numeric.")
            return

        if choice == "Login":
            if bank.login(name, password):
                st.session_state.user = name
                st.session_state.just_logged_in = True
                st.experimental_rerun()
            else:
                st.error("❌ Invalid credentials.")
        else:
            if bank.user_exists(name):
                st.warning("⚠️ User already exists. Try logging in.")
            else:
                bank.register(name, password)
                st.success("✅ Registration successful! Please login now.")

# --- DASHBOARD ---
def dashboard():
    st.sidebar.markdown(f"### 👤 {st.session_state.user.capitalize()}")
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    menu = st.sidebar.radio("📋 Menu", ["🏦 Overview", "➕ Deposit", "➖ Withdraw", "🔁 Transfer", "📜 History", "📈 Analytics", "🚪 Logout"])

    if st.session_state.just_logged_in:
        st.success(f"✅ Welcome back, {st.session_state.user.capitalize()}!")
        st.session_state.just_logged_in = False
        time.sleep(1)

    st.title("💳 Account Dashboard")
    st.balloons()

    balance = bank.get_balance(st.session_state.user)
    st.metric("Available Balance", f"₹{balance}")

    if menu == "➕ Deposit":
        st.subheader("➕ Deposit Money")
        amount = st.number_input("Enter amount", min_value=1)
        if st.button("Deposit"):
            bank.deposit(st.session_state.user, amount)
            st.success(f"✅ ₹{amount} deposited successfully!")

    elif menu == "➖ Withdraw":
        st.subheader("➖ Withdraw Money")
        amount = st.number_input("Enter amount", min_value=1)
        if st.button("Withdraw"):
            if bank.withdraw(st.session_state.user, amount):
                st.success(f"✅ ₹{amount} withdrawn successfully!")
            else:
                st.error("❌ Not enough balance.")

    elif menu == "🔁 Transfer":
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

    elif menu == "📜 History":
        st.subheader("📜 Transaction History")
        history = bank.get_history(st.session_state.user)
        if history:
            for txn in reversed(history[-10:]):
                st.info(txn)
        else:
            st.write("No transactions yet.")

    elif menu == "📈 Analytics":
        st.subheader("📊 Spending & Earning Insights")
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
            fig = px.bar(
                df, x="Transaction Type", y="Count",
                title="Transaction Summary",
                color="Transaction Type",
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            st.plotly_chart(fig)

    elif menu == "🚪 Logout":
        st.session_state.user = None
        st.session_state.just_logged_in = False
        st.success("✅ Logged out.")
        time.sleep(1)
        st.experimental_rerun()

# --- MAIN ---
if st.session_state.user:
    dashboard()
else:
    login_section()

