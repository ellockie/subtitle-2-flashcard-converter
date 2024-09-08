import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath("../config/"))))

from config.config_light import ConfigLight
from utils.ask_user_for_video_name import ask_user_for_video_name
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


def main():
    config = ConfigLight()
    config.video_name = ask_user_for_video_name(None)
    url = input("\n  Enter the URL of the file to download: ")
    download_file(url, SUBTITLES_FILENAME)
    FileHandler(config)


if __name__ == "__main__":
    main()
else:
    print(f"__name__:  {__name__}")
