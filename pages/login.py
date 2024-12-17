import customtkinter as ctk
import time
import tkinter as tk
import json
import os  # Fix: Missing import


# LoginPage
class LoginPage(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # Title Label
        self.title_label = ctk.CTkLabel(self, text="Login", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Username and Password Entry
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.grid(row=1, column=0, padx=20, pady=(10, 10), sticky="ew")

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")

        # Login Button
        self.login_button = ctk.CTkButton(self, text="Login", command=self.login_action)
        self.login_button.grid(row=3, column=0, padx=20, pady=(10, 20), sticky="ew")

        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.grid(row=4, column=0, padx=20, pady=(0, 10))

    def login_action(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            with open("data/users.json", "r") as f:
                data = json.load(f)
                users = data.get("users", [])

            for user in users:
                if user["username"] == username and user["password"] == password:
                    self.error_label.configure(text="")
                    self.master.switch_to_main_app(username)
                    return

            self.error_label.configure(text="Invalid username or password.")
        except FileNotFoundError:
            self.error_label.configure(text="No registered users found.")
