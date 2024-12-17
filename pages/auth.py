import customtkinter as ctk
import time
import tkinter as tk
import json
import os  # Fix: Missing import


class MainFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Welcome Label
        self.title_label = ctk.CTkLabel(self, text="Welcome!", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Login Button
        self.login_button = ctk.CTkButton(self, text="Login", command=master.switch_to_login)
        self.login_button.grid(row=1, column=0, padx=20, pady=(10, 10))

        # Signup Button
        self.signup_button = ctk.CTkButton(self, text="Signup", command=master.switch_to_signup)
        self.signup_button.grid(row=2, column=0, padx=20, pady=(10, 20))
