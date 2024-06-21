import re


REGEX = {
    "WEBVTT_BLOCK": [r'^(WEBVTT.*\n)*(X-TIMESTAMP-MAP=.*\n)*\n', ''],
    "CLEANING": [r'^\d+\s*\n(\d{2}:\d{2}:\d{2}[,\.]\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}[,\.]\d{3})\s*\n', ''],
    "NEWLINE_REMOVAL": [r'(?<!\n)\n(?!\n)', ' '],
    "JOIN_DOUBLE_NEWLINES": [r'\n{2,}', ' '],
}

def process_subtitles(subtitle_text):
    """Process subtitle text to convert it into paragraphs."""
    # Remove the initial WEBVTT block and any subsequent metadata before the first subtitle block
    subtitle_text = re.sub(REGEX["WEBVTT_BLOCK"][0], REGEX["WEBVTT_BLOCK"][1], subtitle_text, flags=re.MULTILINE)

    # Remove subtitle numbers and timestamps
    cleaned_text = re.sub(REGEX["CLEANING"][0], REGEX["CLEANING"][1], subtitle_text, flags=re.MULTILINE)

    # Replace single newlines within subtitle blocks with spaces
    cleaned_text = re.sub(REGEX["NEWLINE_REMOVAL"][0], REGEX["NEWLINE_REMOVAL"][1], cleaned_text)

    # Replace double newlines with a space to form paragraphs
    paragraph_text = re.sub(REGEX["JOIN_DOUBLE_NEWLINES"][0], REGEX["JOIN_DOUBLE_NEWLINES"][1], cleaned_text).strip()

    return paragraph_text


def load_and_process_file(input_file, output_file):
    """Load subtitle text from input file, process it, and save the result to output file."""
    with open(input_file, 'r', encoding='utf-8') as file:
        subtitle_text = file.read()

    # Process the subtitle text
    paragraph_text = process_subtitles(subtitle_text)

    # Write the result to output file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(paragraph_text)


def main():
    input_file = '_input.txt'
    output_file = '_output.txt'
    load_and_process_file(input_file, output_file)
    print(f"Subtitle text has been converted and saved to {output_file}")


if __name__ == "__main__":
    main()
