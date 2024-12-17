import customtkinter as ctk
import time
import tkinter as tk
import json
import os  # Fix: Missing import



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
            with open("data/sentences.json", "r") as f:
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
        result_data = {
            "username": self.username,
            "time": self.elapsed_time,
            "characters": self.characters,
            "words": self.words,
            "cpm": self.cpm,
            "wpm": self.wpm,
            "accuracy": self.accuracy,
            "text": self.texts[self.current_text_index]  # Include the text used in the test
        }
        self.save_result_to_json(result_data)
    def save_result_to_json(self, result_data):
        try:
            with open("data/results.json", "r") as f:
                results = json.load(f)
        except FileNotFoundError:
            results = []

        results.append(result_data)

        with open("data/results.json", "w") as f:
            json.dump(results, f, indent=4)


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

