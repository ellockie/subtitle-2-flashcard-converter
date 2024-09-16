import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

from utils.downloader import submit
from utils.summary_checker import check_for_new_summary, copy_to_clipboard


def run_app():

    print("() @run_app()")
    # Create main window
    root = tk.Tk()
    root.title("Subtitle Downloader")

    # Load the image using Pillow
    # image_path = os.path.join(os.path.dirname(__file__), "images", "app-icon.png")
    # image = Image.open(image_path)
    image = Image.open("images/app-icon.png")
    icon = ImageTk.PhotoImage(image)

    print("() Icon loaded")

    # Set the window icon
    root.iconphoto(True, icon)

    # Set window size
    root.geometry("1222x800")  # Adjusted height to accommodate the text widget

    # Video Name Input
    video_name_label = ttk.Label(root, text="Video Name:")
    video_name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    video_name_entry = ttk.Entry(root)
    video_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    video_name_entry.bind(
        "<FocusIn>", lambda event: video_name_entry.selection_range(0, tk.END)
    )

    # URL Input
    url_label = ttk.Label(root, text="Subtitle URL:")
    url_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

    url_entry = ttk.Entry(root)
    url_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
    url_entry.bind("<FocusIn>", lambda event: url_entry.selection_range(0, tk.END))

    # Configure column weights to expand entry fields
    root.columnconfigure(1, weight=1)

    # Submit Button
    submit_button = ttk.Button(
        root, text="Submit", command=lambda: submit(video_name_entry, url_entry)
    )
    submit_button.grid(row=2, column=0, columnspan=2, pady=10)

    # Summary Text Widget
    summary_text_widget = tk.Text(root, wrap="word", height=20)
    summary_text_widget.grid(
        row=3, column=0, columnspan=2, padx=5, pady=5, sticky="nsew"
    )

    # Configure row weight for the text widget to expand
    root.rowconfigure(3, weight=1)

    # Copy to Clipboard Button
    copy_button = ttk.Button(
        root,
        text="Copy to Clipboard",
        command=lambda: copy_to_clipboard(
            root, summary_text_widget, confirmation_label
        ),
    )
    copy_button.grid(row=4, column=0, columnspan=2, pady=5)

    # Confirmation Message Label
    confirmation_label = ttk.Label(root, text="")
    confirmation_label.grid(row=5, column=0, columnspan=2)

    # Start checking for new summary files
    check_for_new_summary(root, summary_text_widget)

    root.mainloop()
