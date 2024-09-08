import requests
import sys
import os
import tkinter as tk
from tkinter import ttk

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath("../config/"))))

from config.config_light import ConfigLight
from utils.file_handler import FileHandler

SUBTITLES_FILENAME = "_input_subtitles.txt"


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
    url = url_entry.get()

    if not video_name or not url:
        print("\n  Please enter both video name and URL.")
        return

    config = ConfigLight()
    config.video_name = video_name

    try:
        download_file(url, SUBTITLES_FILENAME)
        FileHandler(config)
    except Exception as e:
        print(f"\n  An error occurred: {e}")


# def main():

# Create main window
root = tk.Tk()
root.title("Subtitle Downloader")

# Video Name Input
video_name_label = ttk.Label(root, text="Video Name:")
video_name_label.grid(row=0, column=0, padx=5, pady=5)

video_name_entry = ttk.Entry(root)
video_name_entry.grid(row=0, column=1, padx=5, pady=5)
video_name_entry.bind(
    "<FocusIn>", lambda event: video_name_entry.selection_range(0, tk.END)
)

# URL Input
url_label = ttk.Label(root, text="Subtitle URL:")
url_label.grid(row=1, column=0, padx=5, pady=5)

url_entry = ttk.Entry(root)
url_entry.grid(row=1, column=1, padx=5, pady=5)
url_entry.bind("<FocusIn>", lambda event: url_entry.selection_range(0, tk.END))

# Submit Button
submit_button = ttk.Button(root, text="Submit", command=submit)
submit_button.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()


# if __name__ == "__main__":
#     main()
# else:
#     print(f"__name__:  {__name__}")
