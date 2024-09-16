import requests
import urllib
import subprocess
import sys
import os
import re
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath("../config/"))))

from config.config_light import ConfigLight
from utils.file_handler import FileHandler

SUBTITLES_FILENAME = "_input_subtitles.txt"

last_loaded_version = -1  # Global variable to keep track of the latest loaded version
last_filepath = ""


def download_file(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"\n  File downloaded successfully as '{filename}'")
    except requests.exceptions.RequestException as e:
        print(f"\n  An error occurred while downloading the file: {e}")
        raise e


def submit():
    video_name = video_name_entry.get()
    video_name = video_name.strip().replace("	", ". ")
    url = url_entry.get()
    # Sanitize the URL
    url = urllib.parse.unquote(url).strip()

    print(f"\n video_name:  '{video_name}'")
    print(f"        url:  {url}\n")

    if not video_name or not url:
        print("\n  Please enter both video name and URL.")
        return

    config = ConfigLight()
    config.video_name = video_name

    try:
        download_file(url, SUBTITLES_FILENAME)
        FileHandler(config)
        # Run docker-compose up command
        subprocess.run(
            ["docker-compose", "up"], check=True
        )  # check=True raises an error if the command fails

        # Clear form inputs if successful
        video_name_entry.delete(0, tk.END)
        url_entry.delete(0, tk.END)
    except Exception as e:
        print(f"\n  An error occurred: {e}")


def find_latest_summary_file():
    # Assuming the script is in "/src" directory
    results_dir = os.path.abspath(os.path.join("_results"))

    if not os.path.isdir(results_dir):
        print(f"Results directory '{results_dir}' does not exist.")
        return None, None

    # Get the list of folders in the results directory, sorted alphabetically
    folders = sorted(
        [
            d
            for d in os.listdir(results_dir)
            if os.path.isdir(os.path.join(results_dir, d))
        ]
    )

    if not folders:
        print(f"No folders found in '{results_dir}'.")
        return None, None

    # Get the alphabetically last folder
    last_folder = folders[-1]
    last_folder_path = os.path.join(results_dir, last_folder)

    # Find summary files in the last folder
    summary_files = []
    for f in os.listdir(last_folder_path):
        match = re.match(r"summary_v(\d+)\.txt$", f)
        if match:
            version = int(match.group(1))
            summary_files.append((version, f))

    if not summary_files:
        print(f"No summary files found in '{last_folder_path}'.")
        return None, None

    # Find the file with the highest version number
    latest_version, latest_summary_file = max(summary_files, key=lambda x: x[0])
    latest_summary_file_path = os.path.join(last_folder_path, latest_summary_file)

    return latest_summary_file_path, latest_version


def check_for_new_summary():
    global last_loaded_version, last_filepath
    filepath, version = find_latest_summary_file()
    if filepath is None or version is None:
        # Schedule the function to run again after 5 seconds
        root.after(5000, check_for_new_summary)
        return
    if filepath != last_filepath:
        last_filepath = filepath
        last_loaded_version = 0
        print(
            f"[] version: {version} <= last_loaded_version: {last_loaded_version}.\n   last_filepath: {last_filepath}.\n   filepath: {filepath}"
        )

    if version > last_loaded_version:
        try:
            with open(filepath, "r") as f:
                content = f.read()
            # Update the Text widget
            summary_text_widget.delete("1.0", tk.END)
            summary_text_widget.insert("1.0", content)
            last_loaded_version = version
            print(f"Loaded new summary file version {version}")
        except Exception as e:
            print(f"Failed to read summary file: {e}")

    # Schedule the function to run again after 5 seconds
    root.after(5000, check_for_new_summary)


def copy_to_clipboard():
    content = summary_text_widget.get("1.0", tk.END)
    root.clipboard_clear()
    root.clipboard_append(content)
    # Display confirmation message
    confirmation_label.config(text="Summary copied to clipboard.")
    # Clear the message after 5 seconds
    root.after(5000, lambda: confirmation_label.config(text=""))


# Create main window
root = tk.Tk()
root.title("Subtitle Downloader")

# Load the image using Pillow
image = Image.open("images/app-icon.png")
icon = ImageTk.PhotoImage(image)

# Set the window icon
root.iconphoto(True, icon)

# Set window size
root.geometry("1222x800")  # Adjusted height to accommodate the text widget

# Video Name Input
video_name_label = ttk.Label(root, text="Video Name:")
video_name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

video_name_entry = ttk.Entry(root)
video_name_entry.grid(
    row=0, column=1, padx=5, pady=5, sticky="ew"
)  # Expand horizontally
video_name_entry.bind(
    "<FocusIn>", lambda event: video_name_entry.selection_range(0, tk.END)
)

# URL Input
url_label = ttk.Label(root, text="Subtitle URL:")
url_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

url_entry = ttk.Entry(root)
url_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")  # Expand horizontally
url_entry.bind("<FocusIn>", lambda event: url_entry.selection_range(0, tk.END))

# Configure column weights to expand entry fields
root.columnconfigure(1, weight=1)

# Submit Button
submit_button = ttk.Button(root, text="Submit", command=submit)
submit_button.grid(row=2, column=0, columnspan=2, pady=10)

# Summary Text Widget
summary_text_widget = tk.Text(root, wrap="word", height=20)
summary_text_widget.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

# Configure row weight for the text widget to expand
root.rowconfigure(3, weight=1)

# Copy to Clipboard Button
copy_button = ttk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.grid(row=4, column=0, columnspan=2, pady=5)

# Confirmation Message Label
confirmation_label = ttk.Label(root, text="")
confirmation_label.grid(row=5, column=0, columnspan=2)

# Start checking for new summary files
check_for_new_summary()

root.mainloop()
