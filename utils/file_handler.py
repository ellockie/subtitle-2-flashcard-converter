import os
import hashlib
from datetime import datetime
import shutil

from constants.constants import OUTPUT_TYPE
from utils.ask_user_for_video_name import ask_user_for_video_name


class FileHandler:
    def __init__(self, config):
        self.config = config
        self.results_folder = "_results"
        self._ensure_results_folder_exists()
        self.input_hash = self._calculate_input_hash()
        self.video_name = config.video_name
        self.output_folder = self._create_output_folder()
        self._copy_input_file()

    def _ensure_results_folder_exists(self):
        """Create the _results folder if it doesn't exist."""
        if not os.path.exists(self.results_folder):
            os.makedirs(self.results_folder)
            print(f"Created {self.results_folder} folder")

    def _calculate_input_hash(self):
        with open(self.config.input_file, "rb") as file:
            return hashlib.md5(file.read()).hexdigest()[:8]

    def _create_output_folder(self):
        date_str = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
        default_folder_name = f"{date_str}__{self.input_hash}"

        # Check if a folder with this hash already exists
        existing_folders = [
            f
            for f in os.listdir(self.results_folder)
            if f.find(f"__{self.input_hash}") >= 0
        ]
        if existing_folders:
            folder_name = existing_folders[0]  # Use the existing folder
        else:
            # Try to get user input, fall back to default if not possible
            try:
                if not self.video_name:
                    self.video_name = ask_user_for_video_name(default_folder_name)
                folder_name = (
                    f"{default_folder_name} - {self.video_name}"
                    if self.video_name
                    else default_folder_name
                )
            except EOFError:
                print(
                    f"Running in non-interactive environment. Using default folder name: {default_folder_name}"
                )
                folder_name = default_folder_name

        full_path = os.path.join(self.results_folder, folder_name)
        os.makedirs(full_path, exist_ok=True)

        # Create QA sets subfolder
        qa_sets_path = os.path.join(
            self.results_folder, folder_name, self.config.qa_sets_subfolder
        )
        os.makedirs(qa_sets_path, exist_ok=True)

        return full_path

    def _copy_input_file(self):
        """Copy the input file to the output folder if it exists."""
        if os.path.exists(self.config.input_file):
            destination = os.path.join(self.output_folder, self.config.raw_input_file)
            shutil.copy2(self.config.input_file, destination)
            print(f"Copied input file to {destination}")
        else:
            print(
                f"Warning: Input file {self.config.input_file} not found. Skipping copy."
            )

    def save_output(self, output, output_file, output_type):
        """Save the generated output to the specified output file."""
        file_name = os.path.basename(output_file)
        if output_type == OUTPUT_TYPE["QAs"]:
            full_path = os.path.join(
                self.output_folder, self.config.qa_sets_subfolder, file_name
            )
        else:
            full_path = os.path.join(self.output_folder, file_name)

        if file_name == self.config.qa_file or file_name == self.config.summary_file:
            full_path = self._get_versioned_filename(full_path)

        with open(full_path, "w", encoding="utf-8") as file:
            file.write(output)
        print(f"{output_type} saved to {full_path}")

    def _get_versioned_filename(self, file_path):
        base, ext = os.path.splitext(file_path)
        version = 1
        while os.path.exists(f"{base}_v{version}{ext}"):
            version += 1
        return f"{base}_v{version}{ext}"

    def add_description(self, description):
        """Add a description to the output folder name."""
        current_name = os.path.basename(self.output_folder)
        new_name = f"{current_name}__{description}"
        new_path = os.path.join(self.results_folder, new_name)
        os.rename(self.output_folder, new_path)
        self.output_folder = new_path
        print(f"Added description to output folder: {new_name}")
