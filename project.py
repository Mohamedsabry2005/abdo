import customtkinter as ctk
import time
import tkinter as tk
import json
import os  # Fix: Missing import

from pages.main import MainPage
from pages.login import LoginPage
from pages.signup import SignupPage
from pages.auth import MainFrame



class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Speed Test App")
        self.geometry("400x500")

        self.main_frame = MainFrame(master=self)
        self.main_frame.pack(fill="both", expand=True)

        self.login_page = LoginPage(master=self)
        self.signup_page = SignupPage(master=self)

    def switch_to_login(self):
        self.main_frame.pack_forget()
        self.signup_page.pack_forget()
        self.login_page.pack(fill="both", expand=True)

    def switch_to_signup(self):
        self.main_frame.pack_forget()
        self.login_page.pack_forget()
        self.signup_page.pack(fill="both", expand=True)

    def switch_to_main(self):
        self.login_page.pack_forget()
        self.signup_page.pack_forget()
        self.main_frame.pack(fill="both", expand=True)

    def switch_to_main_app(self, username):
        self.login_page.pack_forget()
        main_page = MainPage(master=self, username=username)
        main_page.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()