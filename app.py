import streamlit as st
from bank_system import BankSystem
from datetime import datetime
import pytz
import json
import time
import pandas as pd
import plotly.express as px

# --- Admin Credentials ---
ADMIN_NAME = "KANAN PANDIT"
ADMIN_PASSWORD = "260300"

# --- Initialize Session ---
st.set_page_config(page_title="Golar Gramin Bank", layout="wide", page_icon="🏦")
bank = BankSystem()

if "user" not in st.session_state:
    st.session_state.user = None
if "acc_no" not in st.session_state:
    st.session_state.acc_no = None

# --- Current Indian Time ---
india_time = datetime.now(pytz.timezone("Asia/Kolkata"))
now = india_time.strftime("%A, %d %B %Y | %I:%M:%S %p")

# --- Navigation Bar ---
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
<style>
.nav-bar {{
    background-color: #003566;
    padding: 10px 20px;
    color: white;
    display: flex;
    justify-content: space-between;
}}
.nav-links a {{
    color: white;
    margin: 0 10px;
    text-decoration: none;
}}
.nav-links a:hover {{
    color: #ffd60a;
}}
.quote-banner {{
    background-color: #ffd60a;
    color: #003566;
    font-size: 18px;
    font-weight: 500;
    text-align: center;
    padding: 10px;
    border-radius: 10px;
    margin: 10px 0;
}}
.footer {{
    margin-top: 40px;
    text-align: center;
    font-size: 14px;
    color: #888;
}}
</style>
<div class="nav-bar">
    <div><strong>🌐 Golar Gramin Bank</strong></div>
    <div class="nav-links">{nav_links}</div>
    <div>🕒 {now}</div>
</div>
<div class="quote-banner">
    “The ultimate goal of banking is not just saving money, but empowering lives and communities.”
</div>
""", unsafe_allow_html=True)

# --- Login / Register / Forgot Password ---
def login_section():
    st.markdown("## 🔐 Login / Register / Forgot Password")
    option = st.radio("Choose an option", ["Login", "Register", "Forgot Password"], horizontal=True)

    if option == "Register":
        acc = st.text_input("🔢 Account Number (10-digit)")
        name = st.text_input("👤 Full Name (Will be stored in UPPERCASE)")
        password = st.text_input("🔑 Password (6-digit)", type="password")
        mobile = st.text_input("📱 Mobile Number (10-digit)")

        if st.button("Register"):
            success, msg = bank.register(acc, name, password, mobile)
            if success:
                st.success(msg)
            else:
                st.error(msg)

    elif option == "Forgot Password":
        identifier = st.text_input("Enter your registered Name or Mobile Number")
        if st.button("Retrieve Password"):
            pwd = bank.get_password_by_mobile_or_name(identifier)
            if pwd:
                st.success(f"Your password is: **{pwd}**")
            else:
                st.error("User not found. Please check your input.")

    elif option == "Login":
        idn = st.text_input("🧾 Account No / Name / Mobile")
        pwd = st.text_input("🔑 Password (6-digit)", type="password")
        if st.button("Login"):
            if idn.strip().upper() == ADMIN_NAME and pwd == ADMIN_PASSWORD:
                st.session_state.user = ADMIN_NAME
                st.session_state.acc_no = "admin"
                st.success("✅ Admin Logged in!")
                time.sleep(1)
                st.rerun()
            else:
                acc = bank.login(idn.strip(), pwd)
                if acc:
                    st.session_state.user = bank.users[acc]["name"]
                    st.session_state.acc_no = acc
                    st.success(f"🎉 Welcome to Golar Gramin Bank, {st.session_state.user}! Empowering your financial journey with trust and care 💰🏦")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")

# --- Dashboard ---
def dashboard():
    is_admin = st.session_state.user == ADMIN_NAME
    st.sidebar.markdown(f"### 👤 {st.session_state.user}")
    menu = st.sidebar.radio("📋 Menu", 
        ["Dashboard", "Deposit", "Withdraw", "Transfer", "History", "Analytics"] + 
        (["Admin Panel"] if is_admin else []) + ["Logout"]
    )

    acc_no = st.session_state.acc_no

    if menu == "Dashboard":
        st.title("💼 Account Dashboard")
        balance = bank.get_balance(acc_no)
        st.metric("Current Balance", f"₹{balance}")

    elif menu == "Deposit":
        amt = st.number_input("💰 Enter deposit amount", min_value=1)
        if st.button("Deposit"):
            bank.deposit(acc_no, amt)
            st.success(f"₹{amt} deposited successfully!")

    elif menu == "Withdraw":
        amt = st.number_input("💵 Enter withdrawal amount", min_value=1)
        if st.button("Withdraw"):
            if bank.withdraw(acc_no, amt):
                st.success(f"₹{amt} withdrawn successfully!")
            else:
                st.error("❌ Insufficient balance")

    elif menu == "Transfer":
        to = st.text_input("👤 Recipient Name or Mobile")
        amt = st.number_input("💸 Amount to transfer", min_value=1)
        if st.button("Transfer"):
            if bank.transfer(acc_no, to.strip(), amt):
                st.success(f"Transferred ₹{amt} to {to}")
            else:
                st.error("❌ Transfer failed")

    elif menu == "History":
        st.subheader("📜 Transaction History")
        hist = bank.get_history(acc_no)
        if hist:
            for item in reversed(hist[-10:]):
                st.info(item)
        else:
            st.write("No transactions available.")

    elif menu == "Analytics":
        st.subheader("📊 Transaction Summary")
        hist = bank.get_history(acc_no)
        txn_type = {"Deposit": 0, "Withdraw": 0, "Transfer": 0}
        for h in hist:
            for k in txn_type:
                if k.lower() in h.lower():
                    txn_type[k] += 1
        df = pd.DataFrame({"Transaction": txn_type.keys(), "Count": txn_type.values()})
        st.plotly_chart(px.bar(df, x="Transaction", y="Count", title="Your Transactions"))

    elif menu == "Admin Panel" and is_admin:
        st.title("🛠️ Admin Panel")
        try:
            with open("bank_data.json", "r") as f:
                data = json.load(f)
            user_keys = list(data.keys())
            selected = st.selectbox("Select user", user_keys)
            if selected:
                st.json(data[selected])
                new_name = st.text_input("Edit Name", data[selected]["name"])
                new_pass = st.text_input("Edit Password", data[selected]["password"])
                new_bal = st.number_input("Edit Balance", value=data[selected]["balance"])
                new_hist = st.text_area("Edit History", "; ".join(data[selected]["history"]))
                if st.button("💾 Save Changes"):
                    data[selected]["name"] = new_name.upper()
                    data[selected]["password"] = new_pass
                    data[selected]["balance"] = new_bal
                    data[selected]["history"] = [x.strip() for x in new_hist.split(";") if x.strip()]
                    with open("bank_data.json", "w") as f:
                        json.dump(data, f, indent=4)
                    st.success("✅ User data updated")
                    st.rerun()
                st.download_button("⬇️ Download All Data", data=json.dumps(data, indent=4), file_name="bank_data.json")
        except FileNotFoundError:
            st.error("❌ bank_data.json not found.")

    elif menu == "Logout":
        st.session_state.user = None
        st.session_state.acc_no = None
        st.success("You have been logged out")
        time.sleep(1)
        st.rerun()

# --- Main Routing ---
if st.session_state.user:
    dashboard()
else:
    login_section()

# --- Footer ---
st.markdown("""
<style>
.footer-custom {
    background-color: #003566;
    color: white;
    padding: 20px;
    text-align: center;
    font-weight: bold;
    font-size: 16px;
    border-top: 4px solid #ffd60a;
}
.footer-custom a {
    color: #ffd60a;
    font-weight: bold;
    text-decoration: none;
}
.footer-custom a:hover {
    color: #ffa500;
    text-decoration: underline;
}
</style>

<div class="footer-custom">
    Developed by <strong>Kanan Pandit</strong> | <b>Aspiring Data Scientist</b><br>
    📧 kananpandit02@gmail.com | 📞 +91-7384661310<br>
    💼 <a href="https://linkedin.com/in/kananpandit02" target="_blank">LinkedIn</a> |  
    🌐 <a href="https://kananpanditportfolio.netlify.app" target="_blank">Portfolio</a> |  
    🧠 <a href="https://github.com/kananpandit02" target="_blank">GitHub</a>
</div>
""", unsafe_allow_html=True)

