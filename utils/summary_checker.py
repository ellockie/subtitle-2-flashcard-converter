import os
import re
import tkinter as tk

last_loaded_version = -1  # Global variable to keep track of the latest loaded version
last_filepath = ""


def find_latest_summary_file():
    results_dir = os.path.abspath("_results")

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


def check_for_new_summary(root, summary_text_widget):
    global last_loaded_version, last_filepath
    filepath, version = find_latest_summary_file()
    if filepath is None or version is None:
        # Schedule the function to run again after 5 seconds
        root.after(5000, lambda: check_for_new_summary(root, summary_text_widget))
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
    root.after(5000, lambda: check_for_new_summary(root, summary_text_widget))


def copy_to_clipboard(root, summary_text_widget, confirmation_label):
    content = summary_text_widget.get("1.0", tk.END)
    root.clipboard_clear()
    root.clipboard_append(content)
    # Display confirmation message
    confirmation_label.config(text="Summary copied to clipboard.")
    # Clear the message after 5 seconds
    root.after(5000, lambda: confirmation_label.config(text=""))
