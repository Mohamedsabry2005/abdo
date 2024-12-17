import customtkinter as ctk
import time
import tkinter as tk
import json
class LoginPage(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1) # Added row for the title

        # Title Label
        self.title_label = ctk.CTkLabel(self, text="Login", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Frame for inputs to give a "tile" appearance
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1) # Make content expand horizontally

        # Username Label and Entry (Inside the input frame)
        self.username_label = ctk.CTkLabel(self.input_frame, text="Username:")
        self.username_label.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")
        self.username_entry = ctk.CTkEntry(self.input_frame)
        self.username_entry.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")

        # Password Label and Entry (Inside the input frame)
        self.password_label = ctk.CTkLabel(self.input_frame, text="Password:")
        self.password_label.grid(row=3, column=0, padx=20, pady=(10, 0), sticky="w")
        self.password_entry = ctk.CTkEntry(self.input_frame, show="*")  # Hide password
        self.password_entry.grid(row=4, column=0, padx=20, pady=(0, 10), sticky="ew")

        # Login Button
        self.login_button = ctk.CTkButton(self, text="Login", command=self.login_action)
        self.login_button.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="ew")

        # Error Label
        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.grid(row=3, column=0, padx=20, pady=(0, 10))

    def login_action(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            with open('users.json','r') as f:
                data=json.load(f)
                valid_users=data.get('users',[])
            for user in valid_users:
              if user["username"] == username and user["password"] == password:
                self.error_label.configure(text="")
                print("Login Successful")
                self.master.switch_to_main_app(username) # Example of switching to the main app
                return
            self.error_label.configure(text="Invalid username or password.")
        except FileNotFoundError:
            self.error_label.configure(text="users file not found.")


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
        self.target_text = "This is some example text for the text area." # Store the target text

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Heading with dynamic username
        self.heading_label = ctk.CTkLabel(self, text=f"Hello, {self.username}!", font=ctk.CTkFont(size=20, weight="bold"))
        self.heading_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        # Text area
        self.text_area = ctk.CTkTextbox(self, wrap="word", state="disabled") # Initialize text_area here
        self.text_area.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="nsew")

        # Input field with timer start
        self.input_field = ctk.CTkEntry(self)
        self.input_field.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.input_field.bind("<KeyRelease>", self.start_timer) # Start timer on first key press

        # Timer Label
        self.timer_label = ctk.CTkLabel(self, text="Time: 0.00s")
        self.timer_label.grid(row=3, column=0, padx=20, pady=(0, 20))
        self.timer_label.grid_remove() # Hide Timer

        self.timer_running = False
        self.elapsed_time = 0.0

        self.set_text(self.target_text) 

    def start_timer(self, event=None):
        if not self.timer_running:
            self.start_time = time.time()
            self.timer_running = True
            self.timer_label.grid() # Show Timer
            self.update_timer()

    def update_timer(self):
        if self.timer_running:
            self.elapsed_time = time.time() - self.start_time
            self.timer_label.configure(text=f"Time: {self.elapsed_time:.2f}s")
            self.after(10, self.update_timer)  # Update every 10 milliseconds

    def set_text(self, text):
        self.text_area.configure(state="normal") # Enable before setting text
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, text)
        self.text_area.configure(state="disabled") # Disable after setting text

    def stop_timer(self):
      if self.timer_running: # Check if timer is running before stopping
        self.timer_running = False
        elapsed_time = time.time() - self.start_time
        self.calculate_results(elapsed_time)
        self.show_results()

    def calculate_results(self, elapsed_time):
        user_input = self.input_field.get()
        self.characters = len(user_input)
        self.words = len(user_input.split())

        if elapsed_time > 0: # Check to prevent divide by zero
            self.cpm = (self.characters / elapsed_time) * 60
            self.wpm = (self.words / elapsed_time) * 60

        correct_characters = sum(1 for a, b in zip(user_input, self.target_text) if a == b)
        if len(self.target_text) > 0:
            self.accuracy = (correct_characters / len(self.target_text)) * 100
        else:
            self.accuracy = 0 # handle empty target text

    def show_results(self):
        results_text = f"Time: {self.elapsed_time:.2f}s\n" \
                      f"Characters: {self.characters}\n" \
                      f"Words: {self.words}\n" \
                      f"CPM: {self.cpm:.2f}\n" \
                      f"WPM: {self.wpm:.2f}\n" \
                      f"Accuracy: {self.accuracy:.2f}%"
        self.text_area.configure(state="normal")
        self.text_area.insert(tk.END, "\n\n" + results_text) # Append results to the text area
        self.text_area.configure(state="disabled")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Speed Test App")
        self.geometry("400x500")
        self.login_page = LoginPage(master=self)
        self.login_page.pack(fill="both", expand=True)
        self.main_page = None # Placeholder for the main app frame

    def switch_to_main_app(self,username):
        self.geometry('1200x600')
        self.login_page.pack_forget() 

        if self.main_page is None:
            self.geometry('1200x600')
            self.main_page = MainPage(master=self, username=username) 
            self.main_page.set_text("This is some example text for the text area.") 
            back_button = ctk.CTkButton(self.main_page, text="Back to Login", command=self.switch_to_login)
            back_button.grid(row=4, column=0, padx=20, pady=(10, 20))

        self.main_page.pack(fill="both", expand=True)
        self.main_page.input_field.bind("<Return>", lambda event:self.main_page.stop_timer()) 

    def switch_to_login(self):
        if self.main_page:
            self.geometry("400x500")
            self.main_page.stop_timer()
            self.main_page.pack_forget()
        self.login_page.pack(fill="both", expand=True)
app = App()
app.mainloop()