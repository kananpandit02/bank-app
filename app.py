# app.py
import streamlit as st
from bank_system import BankSystem

st.set_page_config(page_title="Bank App", layout="centered")
bank = BankSystem()

# Initialize session state
if "user" not in st.session_state:
    st.session_state.user = None

def login_section():
    st.title("🔐 Welcome to MyBank")

    choice = st.radio("Login or Register", ["Login", "Register"])

    name = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Submit"):
        if choice == "Login":
            if bank.login(name, int(password)):
                st.session_state.user = name
                st.success("✅ Logged in!")
            else:
                st.error("❌ Invalid credentials.")
        else:
            if bank.user_exists(name):
                st.warning("⚠️ User already exists.")
            else:
                bank.register(name, int(password))
                st.success("✅ Registration successful. Please login.")

def dashboard():
    st.sidebar.title(f"👤 {st.session_state.user}")
    st.title("🏦 Bank Dashboard")
    balance = bank.get_balance(st.session_state.user)
    st.metric("💳 Current Balance", f"₹{balance}")

    menu = st.sidebar.radio("Select Action", ["Deposit", "Withdraw", "Transfer", "History", "Logout"])

    if menu == "Deposit":
        amount = st.number_input("Enter amount to deposit", min_value=1)
        if st.button("Deposit"):
            bank.deposit(st.session_state.user, amount)
            st.success(f"Deposited ₹{amount}")

    elif menu == "Withdraw":
        amount = st.number_input("Enter amount to withdraw", min_value=1)
        if st.button("Withdraw"):
            success = bank.withdraw(st.session_state.user, amount)
            if success:
                st.success(f"Withdrawn ₹{amount}")
            else:
                st.error("❌ Insufficient funds.")

    elif menu == "Transfer":
        recipient = st.text_input("Recipient Username")
        amount = st.number_input("Amount to transfer", min_value=1)
        if st.button("Transfer"):
            if recipient == st.session_state.user:
                st.warning("⚠️ You can't transfer to yourself.")
            else:
                success = bank.transfer(st.session_state.user, recipient, amount)
                if success:
                    st.success(f"Transferred ₹{amount} to {recipient}")
                else:
                    st.error("❌ Failed. Check balance or recipient.")

    elif menu == "History":
        st.subheader("📜 Transaction History")
        history = bank.get_history(st.session_state.user)
        for item in reversed(history[-10:]):
            st.info(item)

    elif menu == "Logout":
        st.session_state.user = None
        st.success("Logged out.")

# Main view
if st.session_state.user:
    dashboard()
else:
    login_section()
