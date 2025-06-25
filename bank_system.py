import json
import os
from datetime import datetime

class BankSystem:
    def __init__(self):
        self.filename = "users.json"
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists(self.filename):
            return {}
        with open(self.filename, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}

    def save_users(self):
        with open(self.filename, "w") as f:
            json.dump(self.users, f, indent=4)

    def user_exists(self, username):
        return username in self.users

    def register(self, username, password):
        self.users[username] = {
            "password": password,
            "balance": 0,
            "history": []
        }
        self.save_users()

    def login(self, username, password):
        return username in self.users and self.users[username]["password"] == password

    def get_balance(self, username):
        return self.users[username]["balance"]

    def deposit(self, username, amount):
        self.users[username]["balance"] += amount
        self._log(username, f"Deposited ₹{amount}")
        self.save_users()

    def withdraw(self, username, amount):
        if self.users[username]["balance"] >= amount:
            self.users[username]["balance"] -= amount
            self._log(username, f"Withdrew ₹{amount}")
            self.save_users()
            return True
        return False

    def transfer(self, sender, recipient, amount):
        if recipient not in self.users or self.users[sender]["balance"] < amount:
            return False
        self.users[sender]["balance"] -= amount
        self.users[recipient]["balance"] += amount
        self._log(sender, f"Transferred ₹{amount} to {recipient}")
        self._log(recipient, f"Received ₹{amount} from {sender}")
        self.save_users()
        return True

    def get_history(self, username):
        return self.users[username]["history"]

    def _log(self, username, action):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.users[username]["history"].append(f"[{timestamp}] {action}")
