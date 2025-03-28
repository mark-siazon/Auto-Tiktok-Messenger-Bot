import tkinter as tk
from tkinter import messagebox
import threading
import json
import os
from core.messenger import start_bot

# Load the current config (browser choice + remember me setting)
def load_config():
    try:
        with open("config.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"browser_choice": "Brave", "remember_choice": False}

# Save the user config (browser choice + remember me setting)
def save_config(browser_choice, remember_choice):
    config = {"browser_choice": browser_choice, "remember_choice": remember_choice}
    with open("config.json", "w") as file:
        json.dump(config, file, indent=4)

# Check if the browser is installed at the specified location
def check_browser_installed(browser_choice):
    browser_paths = {
        "Brave": "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",
        "Chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "Edge": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
    }

    return os.path.exists(browser_paths.get(browser_choice, ""))

# GUI for browser choice
def browser_choice_gui():
    config = load_config()

    # Create the main window
    root = tk.Tk()
    root.title("Tiktok Auto Messenger | Select Browser")
    root.geometry("400x300")
    root.resizable(True, True)  # Make the window resizable
    
    # Label
    label = tk.Label(root, text="Select the browser you are using:", font=("Arial", 12))
    label.pack(pady=10, padx=20)

    # Radio buttons for browser choice
    browser_var = tk.StringVar(value=config["browser_choice"])
    browsers = ["Brave", "Chrome", "Edge"]
    for browser in browsers:
        tk.Radiobutton(root, text=browser, variable=browser_var, value=browser, font=("Arial", 10)).pack()

    # Remember me checkbox
    remember_var = tk.BooleanVar(value=config["remember_choice"])
    remember_checkbox = tk.Checkbutton(root, text="Remember my choice", variable=remember_var, font=("Arial", 10))
    remember_checkbox.pack(pady=5)

    # Status label
    status_label = tk.Label(root, text="", font=("Arial", 11))
    status_label.pack(pady=10)

    # Start button for the bot
    def start_bot_with_choice():
        # Save the user's choice before starting the bot
        save_config(browser_var.get(), remember_var.get())

        # Check if the selected browser is installed
        if not check_browser_installed(browser_var.get()):
            messagebox.showerror("Error", f"{browser_var.get()} browser not found at the specified location.")
            return

        # Disable the button and make a status message
        start_button.config(state=tk.DISABLED, text="Bot is Running...")
        status_label.config(text="Bot is starting... Please wait.")

        # Start the bot in a new thread
        threading.Thread(target=start_bot, daemon=True).start()

        # Keep the window open until the bot finishes
        root.after(1000, check_bot_running)

    def check_bot_running():
        # If bot is running, don't close the window
        if threading.active_count() > 1:
            root.after(1000, check_bot_running)
        else:
            status_label.config(text="Bot finished. You can close the window.")
            start_button.config(state=tk.NORMAL, text="Start Messaging")

    start_button = tk.Button(root, text="Start Messaging", font=("Arial", 12), command=start_bot_with_choice)
    start_button.pack(pady=20)

    root.mainloop()

# Entry point
if __name__ == "__main__":
    browser_choice_gui()
