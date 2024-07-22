import re
import os

from constants.constants import OUTPUT_TYPE


class SubtitleProcessor:
    def __init__(self, config, file_handler):
        self.config = config
        self.file_handler = file_handler
        # Define regex patterns for subtitle processing
        self.REGEXES = [
            # Remove the initial WEBVTT block and any subsequent metadata before the first subtitle block
            (r'^(WEBVTT.*\n)*(X-TIMESTAMP-MAP=.*\n)*\n', '', re.MULTILINE),
            # Remove subtitle numbers and timestamps
            (r'^\d+\s*\n(\d{2}:\d{2}:\d{2}[,\.]\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}[,\.]\d{3})\s*\n', '', re.MULTILINE),
            # Replace single newlines within subtitle blocks with spaces
            (r'(?<!\n)\n(?!\n)', ' '),
            # Replace double newlines with a space to form paragraphs
            (r'\n{2,}', ' '),
            # Inserts two newlines after each full stop followed by a space and a non-whitespace character
            (r'(\.\s*)(?=\S)', '.\n\n')
        ]

    def get_plain_text_from_subtitles(self):
        """Load subtitle text from input file and process it, or load from processed file if it exists."""
        if os.path.exists(self.config.processed_text_file):
            print(f"Loading processed text from existing file: {self.config.processed_text_file}")
            with open(self.config.processed_text_file, 'r', encoding='utf-8') as file:
                return file.read()

        print(f"Processing subtitle file: {self.config.input_file}")
        with open(self.config.input_file, 'r', encoding='utf-8') as file:
            subtitle_text = file.read()
        plain_text = self._process_subtitles(subtitle_text)
        self.file_handler.save_output(plain_text, self.config.processed_text_file, OUTPUT_TYPE["Processed text"])
        return plain_text

    def _process_subtitles(self, subtitle_text):
        """Process subtitle text to convert it into paragraphs."""
        for pattern, repl, *flags in self.REGEXES:
            flags = flags[0] if flags else 0
            subtitle_text = re.sub(pattern, repl, subtitle_text, flags=flags)
        return subtitle_text.strip()
