import streamlit as st
from bank_system import BankSystem
from datetime import datetime
import json
import time
import plotly.express as px
import pandas as pd

ADMIN_NAME = "Kanan Pandit"
ADMIN_PASSWORD = "260300"
ADMIN_CONTACT = "📧 kananpandit02@gmail.com | 📱 +91-XXXXXXXXXX"

st.set_page_config(page_title="Golar Gramin Bank", layout="wide", page_icon="🏦")
bank = BankSystem()

if "user" not in st.session_state:
    st.session_state.user = None
if "acc_no" not in st.session_state:
    st.session_state.acc_no = None

now = datetime.now().strftime("%A, %d %B %Y | %I:%M:%S %p")

# Navbar
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
</style>
<div class="nav-bar">
  <div><strong>🏦 Golar Gramin Bank</strong></div>
  <div class="nav-links">{nav_links}</div>
  <div>🕒 {now}</div>
</div>
<div class="quote-banner">"Empowering lives through digital banking."</div>
""", unsafe_allow_html=True)

# Login/Register Section
def login_section():
    st.markdown("## 👤 Login or Register")
    tab1, tab2, tab3 = st.tabs(["🔐 User Login", "📝 Register", "🔑 Forgot Password"])

    with tab1:
        identifier = st.text_input("Account No / Username / Mobile")
        password = st.text_input("Password (6-digit)", type="password")
        if st.button("Login"):
            if identifier == ADMIN_NAME and password == ADMIN_PASSWORD:
                st.session_state.user = ADMIN_NAME
                st.session_state.acc_no = "admin"
                st.success("✅ Welcome Admin!")
                time.sleep(1)
                st.rerun()
            else:
                acc_no = bank.login(identifier, password)
                if acc_no:
                    st.session_state.user = bank.users[acc_no]["name"]
                    st.session_state.acc_no = acc_no
                    st.success(f"✅ Welcome {st.session_state.user}!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")

    with tab2:
        acc_no = st.text_input("Account Number (10 digits)")
        name = st.text_input("Full Name (will be saved in CAPS)")
        mobile = st.text_input("Mobile Number")
        password = st.text_input("Password (6-digit)", type="password")
        if st.button("Register"):
            success, msg = bank.register(acc_no, name, password, mobile)
            st.success(msg) if success else st.error(msg)

    with tab3:
        query = st.text_input("Enter Registered Mobile or Name (in CAPS)")
        if st.button("Recover Password"):
            pw = bank.forgot_password(query)
            if pw:
                st.info(f"🔑 Your password is: {pw}")
            else:
                st.error("❌ No matching user found")

# Dashboard
def dashboard():
    st.sidebar.title("🏦 Menu")
    st.sidebar.markdown(f"**👤 {st.session_state.user}**")
    is_admin = st.session_state.user == ADMIN_NAME
    menu = st.sidebar.radio("Select", ["Dashboard", "Deposit", "Withdraw", "Transfer", "History", "Analytics", "Logout"] + (["Admin Panel"] if is_admin else []))

    acc_no = st.session_state.acc_no

    if menu == "Dashboard":
        st.title("💼 Account Dashboard")
        st.metric("Available Balance", f"₹{bank.get_balance(acc_no)}")

    elif menu == "Deposit":
        amt = st.number_input("Enter amount to deposit", min_value=1)
        if st.button("Deposit"):
            bank.deposit(acc_no, amt)
            st.success(f"Deposited ₹{amt}")

    elif menu == "Withdraw":
        amt = st.number_input("Enter amount to withdraw", min_value=1)
        if st.button("Withdraw"):
            if bank.withdraw(acc_no, amt):
                st.success(f"Withdrew ₹{amt}")
            else:
                st.error("Insufficient balance")

    elif menu == "Transfer":
        to = st.text_input("Recipient (Name or Mobile)")
        amt = st.number_input("Amount to transfer", min_value=1)
        if st.button("Transfer"):
            if to.upper() == st.session_state.user or to == bank.users[acc_no]["mobile"]:
                st.warning("Cannot transfer to self")
            elif bank.transfer(acc_no, to, amt):
                st.success(f"Transferred ₹{amt} to {to}")
            else:
                st.error("Transfer failed")

    elif menu == "History":
        st.subheader("Transaction History")
        for h in reversed(bank.get_history(acc_no)[-10:]):
            st.info(h)

    elif menu == "Analytics":
        history = bank.get_history(acc_no)
        if not history:
            st.warning("No transactions")
        else:
            counts = {"Deposit": 0, "Withdraw": 0, "Transfer": 0}
            for h in history:
                for k in counts:
                    if k.lower() in h.lower():
                        counts[k] += 1
            df = pd.DataFrame({"Transaction": counts.keys(), "Count": counts.values()})
            st.plotly_chart(px.pie(df, names="Transaction", values="Count", title="Transaction Breakdown"))

    elif menu == "Admin Panel":
        st.title("🛠️ Admin Panel")
        st.write("🔒 Admin can edit user data below:")
        try:
            with open("bank_data.json", "r") as f:
                data = json.load(f)
            user_ids = list(data.keys())
            user_id = st.selectbox("Select user", user_ids)
            user = data[user_id]
            new_name = st.text_input("Name", user["name"])
            new_pass = st.text_input("Password", user["password"])
            new_mobile = st.text_input("Mobile", user["mobile"])
            new_bal = st.number_input("Balance", value=user["balance"], min_value=0)
            new_hist = st.text_area("History (semicolon-separated)", value="; ".join(user["history"]))
            if st.button("Save"):
                data[user_id] = {
                    "name": new_name.upper(),
                    "password": new_pass,
                    "mobile": new_mobile,
                    "balance": new_bal,
                    "history": [i.strip() for i in new_hist.split(";") if i.strip()]
                }
                with open("bank_data.json", "w") as f:
                    json.dump(data, f, indent=4)
                st.success("User updated!")
                st.rerun()
        except:
            st.error("Error loading bank_data.json")

    elif menu == "Logout":
        st.session_state.user = None
        st.session_state.acc_no = None
        st.success("Logged out")
        time.sleep(1)
        st.rerun()

if st.session_state.user:
    dashboard()
else:
    login_section()

st.markdown(f"""
<hr><div style="text-align:center; font-size:14px">
👨‍💻 Developed by <b>Kanan Pandit</b><br>
📧 <a href="mailto:kananpandit02@gmail.com">kananpandit02@gmail.com</a><br>
📞 Admin Help: <b>{ADMIN_CONTACT}</b><br>
<em>“Empowering Digital Banking through Data & Design”</em>
</div>
""", unsafe_allow_html=True)
