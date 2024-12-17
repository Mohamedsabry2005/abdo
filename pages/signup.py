import customtkinter as ctk
import time
import tkinter as tk
import json
import os  # Fix: Missing import


# SignupPage: Handles user registration
class SignupPage(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

        # Title Label
        self.title_label = ctk.CTkLabel(self, text="Signup", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Username Entry
        self.username_label = ctk.CTkLabel(self, text="Username:")
        self.username_label.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")
        self.username_entry = ctk.CTkEntry(self)
        self.username_entry.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")

        # Password Entry
        self.password_label = ctk.CTkLabel(self, text="Password:")
        self.password_label.grid(row=3, column=0, padx=20, pady=(10, 0), sticky="w")
        self.password_entry = ctk.CTkEntry(self, show="*")
        self.password_entry.grid(row=4, column=0, padx=20, pady=(0, 10), sticky="ew")

        # Signup Button
        self.signup_button = ctk.CTkButton(self, text="Signup", command=self.signup_action)
        self.signup_button.grid(row=5, column=0, padx=20, pady=(10, 10), sticky="ew")

        # Back Button
        self.back_button = ctk.CTkButton(self, text="Back", command=master.switch_to_main)
        self.back_button.grid(row=6, column=0, padx=20, pady=(10, 20), sticky="ew")

        # Error Message
        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.grid(row=7, column=0, padx=20, pady=(0, 10))

    def signup_action(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            self.error_label.configure(text="Please fill in all fields.")
            return

        user_data = {"username": username, "password": password}

        # Save user data to users.json
        if not os.path.exists("users.json"):
            with open("data/users.json", "w") as f:
                json.dump({"users": []}, f)

        with open("data/users.json", "r") as f:
            data = json.load(f)

        for user in data["users"]:
            if user["username"] == username:
                self.error_label.configure(text="Username already exists!")
                return

        data["users"].append(user_data)

        with open("data/users.json", "w") as f:
            json.dump(data, f, indent=4)

        self.error_label.configure(text="Signup successful!", text_color="green")

