# app.py
import streamlit as st
from bank_system import BankSystem
from PIL import Image

st.set_page_config(page_title="MyBank Dashboard", layout="centered", page_icon="💰")
bank = BankSystem()

# Initialize session state
if "user" not in st.session_state:
    st.session_state.user = None

# Optional Logo/Header
st.markdown("""
    <style>
        .main-title {text-align: center; font-size: 38px; font-weight: bold; color: #2c3e50;}
        .stButton > button {
            border-radius: 12px;
            font-size: 16px;
            background-color: #3498db;
            color: white;
        }
        .stRadio > label {
            font-size: 18px;
            font-weight: 500;
        }
    </style>
""", unsafe_allow_html=True)

def login_section():
    st.markdown("<h1 class='main-title'>🔐 Welcome to MyBank</h1>", unsafe_allow_html=True)
    st.markdown("#### Secure, Smart and Simple Banking")

    choice = st.radio("Select an option:", ["Login", "Register"], horizontal=True)
    st.write("---")

    name = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")

    if st.button("Submit"):
        if choice == "Login":
            if bank.login(name, int(password)):
                st.session_state.user = name
                st.success("✅ Logged in successfully!")
            else:
                st.error("❌ Invalid username or password.")
        else:
            if bank.user_exists(name):
                st.warning("⚠️ User already exists. Try logging in.")
            else:
                bank.register(name, int(password))
                st.success("✅ Registration successful. Please login.")

def dashboard():
    st.sidebar.markdown(f"### 👤 {st.session_state.user}")
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    menu = st.sidebar.radio("📋 Select Action", ["🏦 Dashboard", "➕ Deposit", "➖ Withdraw", "🔁 Transfer", "📜 History", "🚪 Logout"])

    st.title("💳 Account Overview")
    balance = bank.get_balance(st.session_state.user)
    st.metric("Current Balance", f"₹{balance}")

    if menu == "➕ Deposit":
        amount = st.number_input("Enter amount to deposit", min_value=1)
        if st.button("Deposit"):
            bank.deposit(st.session_state.user, amount)
            st.success(f"✅ Deposited ₹{amount}")

    elif menu == "➖ Withdraw":
        amount = st.number_input("Enter amount to withdraw", min_value=1)
        if st.button("Withdraw"):
            success = bank.withdraw(st.session_state.user, amount)
            if success:
                st.success(f"✅ Withdrawn ₹{amount}")
            else:
                st.error("❌ Insufficient balance.")

    elif menu == "🔁 Transfer":
        recipient = st.text_input("👤 Recipient Username")
        amount = st.number_input("Amount to transfer", min_value=1)
        if st.button("Transfer"):
            if recipient == st.session_state.user:
                st.warning("⚠️ You can't transfer to yourself.")
            else:
                success = bank.transfer(st.session_state.user, recipient, amount)
                if success:
                    st.success(f"✅ Transferred ₹{amount} to {recipient}")
                else:
                    st.error("❌ Failed. Check recipient and balance.")

    elif menu == "📜 History":
        st.subheader("📜 Transaction History")
        history = bank.get_history(st.session_state.user)
        if history:
            for item in reversed(history[-10:]):
                st.info(item)
        else:
            st.write("No transactions yet.")

    elif menu == "🚪 Logout":
        st.session_state.user = None
        st.success("✅ You have been logged out.")

# Main View
if st.session_state.user:
    dashboard()
else:
    login_section()
