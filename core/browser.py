import subprocess
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import json
import os
import tkinter as tk
from tkinter import messagebox
import webbrowser

# Load the current config (browser choice)
def load_config():
    try:
        with open("config.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"browser_choice": "Brave", "remember_choice": False}

# Function to check if Edge WebDriver is installed
def check_edge_driver_installed():
    webdriver_path = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedgedriver.exe"
    if not os.path.exists(webdriver_path):
        return False
    return True

# Prompt user to download Edge WebDriver
def prompt_download_edge_driver():
    # Show a message box with the URL to download the Edge WebDriver
    response = messagebox.askyesno(
        "Edge WebDriver Not Found",
        "Edge WebDriver is not installed. Would you like to download it now? (It will open in your browser)",
    )
    if response:
        webbrowser.open("https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/")

# Prompt user to move msedgedriver.exe to the required location
def prompt_move_edge_driver():
    response = messagebox.askyesno(
        "Move msedgedriver.exe",
        "To use Edge WebDriver, you need to move the 'msedgedriver.exe' to the location:\n\n"
        "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\n\n"
        "Do you want to continue with this action?",
    )
    if response:
        messagebox.showinfo(
            "Info", 
            "After moving 'msedgedriver.exe', restart the application to use the WebDriver."
        )

# Function to initialize the browser
def init_browser():
    # Load browser config
    config = load_config()
    browser_choice = config["browser_choice"]

    # Kill any existing browser processes to avoid conflicts
    subprocess.call("taskkill /F /IM chrome.exe", shell=True)
    subprocess.call("taskkill /F /IM msedge.exe", shell=True)

    options = Options()

    if browser_choice == "Brave":
        subprocess.call("taskkill /F /IM brave.exe", shell=True)
        options.binary_location = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
        options.add_argument("--user-data-dir=C:\\Users\\marka\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data")
        options.add_argument("--profile-directory=Profile 1")
        browser = uc.Chrome(options=options, headless=False)  # Use undetected_chromedriver for Brave
    elif browser_choice == "Chrome":
        options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        options.add_argument("--user-data-dir=C:\\Users\\marka\\AppData\\Local\\Google\\Chrome\\User Data")
        options.add_argument("--profile-directory=Profile 1")
        browser = uc.Chrome(options=options, headless=False)  # Use undetected_chromedriver for Chrome
    elif browser_choice == "Edge":
        # Check if Edge WebDriver is installed
        if not check_edge_driver_installed():
            prompt_download_edge_driver()  # Prompt the user to install WebDriver
            prompt_move_edge_driver()  # Prompt user to move the msedgedriver.exe
            return None, None  # Exit the function as WebDriver isn't installed yet

        user_data_dir = "C:\\Users\\marka\\AppData\\Local\\Microsoft\\Edge\\User Data"
        profile_path = "Profile 1"  # Choose a profile
        webdriver_path = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedgedriver.exe"  # Edge WebDriver path

        # Ensure WebDriver exists
        if os.path.exists(webdriver_path):
            edge_options = EdgeOptions()
            edge_options.binary_location = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
            edge_options.add_argument(f"--user-data-dir={user_data_dir}")
            edge_options.add_argument(f"--profile-directory={profile_path}")

            # Use the Edge WebDriver
            service = Service(executable_path=webdriver_path)
            browser = webdriver.Edge(service=service, options=edge_options)
        else:
            raise FileNotFoundError(f"Edge WebDriver not found at {webdriver_path}. Please install Edge WebDriver.")

    wait = WebDriverWait(browser, 20)
    return browser, wait
