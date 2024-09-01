import requests

from config import config
from utils.file_handler import FileHandler

SUBTITLES_FILENAME = "_input_subtitles.txt"

def download_file(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"\n  File downloaded successfully as '{filename}'")
    except requests.exceptions.RequestException as e:
        print(f"\n  An error occurred while downloading the file: {e}")
        raise e

def main():
    url = input("\n  Enter the URL of the file to download: ")

    # if os.path.exists(SUBTITLES_FILENAME):
    #     overwrite = input(f"\n  The file '{SUBTITLES_FILENAME}' already exists. Do you want to overwrite it? (y/n): ")
    #     if overwrite.lower() != 'y':
    #         print("\n  Download cancelled.")
    #         return

    download_file(url, SUBTITLES_FILENAME)
    FileHandler(config)

if __name__ == "__main__":
    main()
