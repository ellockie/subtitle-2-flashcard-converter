import re

REGEXES = [
    # Remove the initial WEBVTT block and any subsequent metadata before the first subtitle block
    (r'^(WEBVTT.*\n)*(X-TIMESTAMP-MAP=.*\n)*\n', '', re.MULTILINE),
    # Remove subtitle numbers and timestamps
    (r'^\d+\s*\n(\d{2}:\d{2}:\d{2}[,\.]\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}[,\.]\d{3})\s*\n', '', re.MULTILINE),
    # Replace single newlines within subtitle blocks with spaces
    (r'(?<!\n)\n(?!\n)', ' '),
    # Replace double newlines with a space to form paragraphs
    (r'\n{2,}', ' ')
]

def process_subtitles(subtitle_text):
    """Process subtitle text to convert it into paragraphs."""
    for pattern, repl, *flags in REGEXES:
        flags = flags[0] if flags else 0
        subtitle_text = re.sub(pattern, repl, subtitle_text, flags=flags)
    return subtitle_text.strip()

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
