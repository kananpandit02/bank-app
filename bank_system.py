# import json
# import os
# from datetime import datetime

# class BankSystem:
#     def __init__(self):
#         self.filename = "users.json"
#         self.users = self.load_users()

#     def load_users(self):
#         if not os.path.exists(self.filename):
#             return {}
#         with open(self.filename, "r") as f:
#             try:
#                 return json.load(f)
#             except json.JSONDecodeError:
#                 return {}

#     def save_users(self):
#         with open(self.filename, "w") as f:
#             json.dump(self.users, f, indent=4)

#     def user_exists(self, username):
#         return username in self.users

#     def register(self, username, password):
#         self.users[username] = {
#             "password": password,
#             "balance": 0,
#             "history": []
#         }
#         self.save_users()

#     def login(self, username, password):
#         return username in self.users and self.users[username]["password"] == password

#     def get_balance(self, username):
#         return self.users[username]["balance"]

#     def deposit(self, username, amount):
#         self.users[username]["balance"] += amount
#         self._log(username, f"Deposited ₹{amount}")
#         self.save_users()

#     def withdraw(self, username, amount):
#         if self.users[username]["balance"] >= amount:
#             self.users[username]["balance"] -= amount
#             self._log(username, f"Withdrew ₹{amount}")
#             self.save_users()
#             return True
#         return False

#     def transfer(self, sender, recipient, amount):
#         if recipient not in self.users or self.users[sender]["balance"] < amount:
#             return False
#         self.users[sender]["balance"] -= amount
#         self.users[recipient]["balance"] += amount
#         self._log(sender, f"Transferred ₹{amount} to {recipient}")
#         self._log(recipient, f"Received ₹{amount} from {sender}")
#         self.save_users()
#         return True

#     def get_history(self, username):
#         return self.users[username]["history"]

#     def _log(self, username, action):
#         timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         self.users[username]["history"].append(f"[{timestamp}] {action}")


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

    def register(self, account_no, name, password):
        if not account_no.isdigit() or len(account_no) != 10:
            return False, "Account number must be 10 digits."
        if account_no in self.users:
            return False, "Account number already registered."
        for user in self.users.values():
            if user["name"] == name:
                return False, "Username already exists."

        self.users[account_no] = {
            "name": name,
            "password": str(password),
            "balance": 0,
            "history": []
        }
        self.save()
        return True, "Registration successful!"

    def login(self, identifier, password):
        for acc_no, user in self.users.items():
            if (identifier == acc_no or identifier == user["name"]) and str(user["password"]) == str(password):
                return acc_no  # return the account number as ID
        return None

    def get_balance(self, acc_no):
        return self.users[acc_no]["balance"]

    def deposit(self, acc_no, amount):
        self.users[acc_no]["balance"] += amount
        self.users[acc_no]["history"].append(
            f"{datetime.now()} - Deposited ₹{amount}")
        self.save()

    def withdraw(self, acc_no, amount):
        if self.users[acc_no]["balance"] >= amount:
            self.users[acc_no]["balance"] -= amount
            self.users[acc_no]["history"].append(
                f"{datetime.now()} - Withdrew ₹{amount}")
            self.save()
            return True
        return False

    def transfer(self, sender_acc, recipient_name, amount):
        recipient_acc = None
        for acc, user in self.users.items():
            if user["name"] == recipient_name:
                recipient_acc = acc
                break

        if recipient_acc and self.users[sender_acc]["balance"] >= amount:
            self.users[sender_acc]["balance"] -= amount
            self.users[recipient_acc]["balance"] += amount
            self.users[sender_acc]["history"].append(
                f"{datetime.now()} - Transferred ₹{amount} to {recipient_name}")
            self.users[recipient_acc]["history"].append(
                f"{datetime.now()} - Received ₹{amount} from {self.users[sender_acc]['name']}")
            self.save()
            return True
        return False

    def get_history(self, acc_no):
        return self.users[acc_no]["history"]

    def user_exists(self, name):
        return any(user["name"] == name for user in self.users.values())


