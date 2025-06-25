import json
import os
from datetime import datetime

class BankSystem:
    def __init__(self, data_file="bank_data.json"):
        self.data_file = data_file
        self.users = {}
        self.load()

    def load(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                self.users = json.load(f)

    def save(self):
        with open(self.data_file, "w") as f:
            json.dump(self.users, f, indent=4)

    def register(self, account_no, name, password, mobile):
        if not account_no.isdigit() or len(account_no) != 10:
            return False, "❌ Account number must be 10 digits."
        if not password.isdigit() or len(password) != 6:
            return False, "❌ Password must be 6 digits."
        if account_no in self.users:
            return False, "❌ Account already registered."
        for user in self.users.values():
            if user["name"] == name.upper():
                return False, "❌ Username already exists."
            if user["mobile"] == mobile:
                return False, "❌ Mobile number already registered."

        self.users[account_no] = {
            "name": name.upper(),
            "password": password,
            "mobile": mobile,
            "balance": 0,
            "history": []
        }
        self.save()
        return True, "✅ Registration successful!"

    def login(self, identifier, password):
        for acc_no, user in self.users.items():
            if (identifier == acc_no or
                identifier == user["name"] or
                identifier == user["mobile"]) and user["password"] == password:
                return acc_no
        return None

    def get_balance(self, acc_no):
        return self.users.get(acc_no, {}).get("balance", 0)

    def deposit(self, acc_no, amount):
        if acc_no in self.users:
            self.users[acc_no]["balance"] += amount
            self.users[acc_no]["history"].append(
                f"{datetime.now().strftime('%d-%m-%Y %I:%M %p')} - Deposited ₹{amount}")
            self.save()

    def withdraw(self, acc_no, amount):
        if acc_no in self.users and self.users[acc_no]["balance"] >= amount:
            self.users[acc_no]["balance"] -= amount
            self.users[acc_no]["history"].append(
                f"{datetime.now().strftime('%d-%m-%Y %I:%M %p')} - Withdrew ₹{amount}")
            self.save()
            return True
        return False

    def transfer(self, sender_acc, recipient_identifier, amount):
        recipient_acc = None
        for acc, user in self.users.items():
            if user["name"] == recipient_identifier.upper() or user["mobile"] == recipient_identifier:
                recipient_acc = acc
                break

        if recipient_acc and self.users.get(sender_acc, {}).get("balance", 0) >= amount:
            sender_name = self.users[sender_acc]["name"]
            recipient_name = self.users[recipient_acc]["name"]

            self.users[sender_acc]["balance"] -= amount
            self.users[recipient_acc]["balance"] += amount

            timestamp = datetime.now().strftime('%d-%m-%Y %I:%M %p')
            self.users[sender_acc]["history"].append(
                f"{timestamp} - Transferred ₹{amount} to {recipient_name}")
            self.users[recipient_acc]["history"].append(
                f"{timestamp} - Received ₹{amount} from {sender_name}")

            self.save()
            return True
        return False

    def get_history(self, acc_no):
        return self.users.get(acc_no, {}).get("history", [])

    def user_exists(self, name):
        return any(user["name"] == name.upper() for user in self.users.values())

    def get_password_by_mobile_or_name(self, identifier):
        for user in self.users.values():
            if user["mobile"] == identifier or user["name"] == identifier.upper():
                return user["password"]
        return None

    def get_all_users(self):
        return self.users
