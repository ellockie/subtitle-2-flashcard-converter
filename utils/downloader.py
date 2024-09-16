import requests
import urllib.parse
import os
import subprocess
import tkinter as tk

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


def submit(video_name_entry, url_entry):
    video_name = video_name_entry.get()
    video_name = video_name.strip().replace("\t", ". ")
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
        subprocess.run(["docker-compose", "up"], check=True)
        # Clear form inputs if successful
        video_name_entry.delete(0, tk.END)
        url_entry.delete(0, tk.END)
    except Exception as e:
        print(f"\n  An error occurred: {e}")
