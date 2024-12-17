import customtkinter as ctk
import time
import tkinter as tk
import json
import os  # Fix: Missing import
import random

# MainFrame: Start Page
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
            with open("users.json", "w") as f:
                json.dump({"users": []}, f)

        with open("users.json", "r") as f:
            data = json.load(f)

        for user in data["users"]:
            if user["username"] == username:
                self.error_label.configure(text="Username already exists!")
                return

        data["users"].append(user_data)

        with open("users.json", "w") as f:
            json.dump(data, f, indent=4)

        self.error_label.configure(text="Signup successful!", text_color="green")


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
            with open("users.json", "r") as f:
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




class MainPage(ctk.CTkFrame):
    def __init__(self, master=None, username="", **kwargs):
        super().__init__(master, **kwargs)
        self.username = username
        self.start_time = None

        self.words = 0
        self.characters = 0
        self.wpm = 0.0
        self.cpm = 0.0
        self.accuracy = 0.0
        self.elapsed_time = 0.0

        # Load texts dynamically from JSON
        self.texts = self.load_sentences()
        if not self.texts:  # Default fallback texts in case of error
            self.texts = [
                "This is a fallback text for typing test.",
                "Please ensure the sentences.json file is correctly loaded.",
            ]

        self.current_text_index = 0
        self.test_completed = False  # Tracks if the test is completed

        # Layout setup
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Heading Label
        self.heading_label = ctk.CTkLabel(self, text=f"Hello, {self.username}!", font=ctk.CTkFont(size=20, weight="bold"))
        self.heading_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        # Text Area
        self.text_area = ctk.CTkTextbox(self, wrap="word", state="disabled")
        self.text_area.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="nsew")

        # Input Field
        self.input_field = ctk.CTkEntry(self)
        self.input_field.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.input_field.bind("<KeyRelease>", self.start_timer)
        self.input_field.bind("<Return>", self.on_enter)

        # Timer Label
        self.timer_label = ctk.CTkLabel(self, text="Time: 0.00s")
        self.timer_label.grid(row=3, column=0, padx=20, pady=(0, 20))
        self.timer_label.grid_remove()

        # Restart Button (Hidden until test ends)
        self.restart_button = ctk.CTkButton(self, text="Restart", command=self.restart_test)
        self.restart_button.grid(row=4, column=0, padx=20, pady=(10, 20))
        self.restart_button.grid_remove()

        self.timer_running = False
        self.results = []
        self.set_text(self.texts[self.current_text_index])

    def load_sentences(self):
        """
        Load sentences dynamically from a JSON file.
        """
        try:
            with open("sentences.json", "r") as f:
                data = json.load(f)
                return data.get("sentences", [])
        except FileNotFoundError:
            print("Error: sentences.json file not found.")
            return []
        except json.JSONDecodeError:
            print("Error: Failed to decode sentences.json.")
            return []

    def start_timer(self, event=None):
        if not self.timer_running and not self.test_completed:
            self.start_time = time.time()
            self.timer_running = True
            self.timer_label.grid()
            self.update_timer()

    def update_timer(self):
        if self.timer_running:
            self.elapsed_time = time.time() - self.start_time
            self.timer_label.configure(text=f"Time: {self.elapsed_time:.2f}s")
            self.after(10, self.update_timer)

    def set_text(self, text):
        self.text_area.configure(state="normal")
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, text)
        self.text_area.configure(state="disabled")

    def on_enter(self, event=None):
        if not self.test_completed:
            self.stop_timer()
        else:
            self.restart_test()

    def stop_timer(self):
        if self.timer_running:
            self.timer_running = False
            self.test_completed = True
            elapsed_time = time.time() - self.start_time
            self.calculate_results(elapsed_time)
            self.save_and_display_results()

            # Show Restart Button
            self.restart_button.grid()

    def calculate_results(self, elapsed_time):
        user_input = self.input_field.get()
        self.characters = len(user_input)
        self.words = len(user_input.split())

        if elapsed_time > 0:
            self.cpm = (self.characters / elapsed_time) * 60
            self.wpm = (self.words / elapsed_time) * 60

        correct_characters = sum(1 for a, b in zip(user_input, self.texts[self.current_text_index]) if a == b)
        if len(self.texts[self.current_text_index]) > 0:
            self.accuracy = (correct_characters / len(self.texts[self.current_text_index])) * 100
        else:
            self.accuracy = 0

    def save_and_display_results(self):
        # Display results
        results_text = (
            f"Results:\n"
            f"Time: {self.elapsed_time:.2f}s\n"
            f"Characters: {self.characters}\n"
            f"Words: {self.words}\n"
            f"CPM: {self.cpm:.2f}\n"
            f"WPM: {self.wpm:.2f}\n"
            f"Accuracy: {self.accuracy:.2f}%"
        )

        self.text_area.configure(state="normal")
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, results_text)
        self.text_area.configure(state="disabled")

    def restart_test(self):
        # Reset state
        self.test_completed = False
        self.timer_running = False
        self.elapsed_time = 0.0
        self.words = 0
        self.characters = 0
        self.wpm = 0.0
        self.cpm = 0.0
        self.accuracy = 0.0

        # Reset UI
        self.input_field.delete(0, tk.END)
        self.timer_label.configure(text="Time: 0.00s")
        self.timer_label.grid_remove()
        self.restart_button.grid_remove()

        # Cycle to the next text
        self.current_text_index = (self.current_text_index + 1) % len(self.texts)
        self.set_text(self.texts[self.current_text_index])

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