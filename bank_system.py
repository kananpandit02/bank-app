# bank_system.py
import json
import os
from datetime import datetime

class BankSystem:
    def __init__(self, filename="users.json"):
        self.filename = filename
        self.users = self.load_users()

    def load_users(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}

    def save_users(self):
        with open(self.filename, 'w') as f:
            json.dump(self.users, f, indent=4)

    def log_transaction(self, name, action):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.users[name].setdefault('history', []).append(f"{action} on {timestamp}")
        self.save_users()

    def user_exists(self, name):
        return name in self.users

    def register(self, name, password):
        self.users[name] = {
            'password': password,
            'balance': 1000,
            'history': ["Account created"]
        }
        self.save_users()

    def login(self, name, password):
        user = self.users.get(name)
        return user is not None and user['password'] == password

    def get_balance(self, name):
        return self.users.get(name, {}).get('balance', 0)

    def deposit(self, name, amount):
        if amount > 0:
            self.users[name]['balance'] += amount
            self.log_transaction(name, f"Deposited ₹{amount}")

    def withdraw(self, name, amount):
        if 0 < amount <= self.users[name]['balance']:
            self.users[name]['balance'] -= amount
            self.log_transaction(name, f"Withdrew ₹{amount}")
            return True
        return False

    def transfer(self, sender, recipient, amount):
        if sender == recipient:
            return False
        if recipient not in self.users or self.users[sender]['balance'] < amount:
            return False

        self.users[sender]['balance'] -= amount
        self.users[recipient]['balance'] += amount
        self.log_transaction(sender, f"Transferred ₹{amount} to {recipient}")
        self.log_transaction(recipient, f"Received ₹{amount} from {sender}")
        return True

    def get_history(self, name):
        return self.users.get(name, {}).get('history', [])
