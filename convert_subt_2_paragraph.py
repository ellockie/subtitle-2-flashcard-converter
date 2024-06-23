import re
from openai import OpenAI
import os
from dotenv import load_dotenv
import pprint

# Customizing PrettyPrinter
pp = pprint.PrettyPrinter(indent=4, width=40, depth=2)

# take environment variables from .env.
load_dotenv()

input_file = '_input.txt'
processed_text_file = '_processed_text.txt'
response_file = "_response.txt"
flashcards_file = '_flashcards.txt'

model = "gpt-3.5-turbo"

prompt_static = """Based on the provided subtitles from a video, which is part of an AWS Associate Developer certification preparation course, create a set of flashcards of any item of knowledge that may be checked in the AWS Associate Developer exam.

Generate flashcards in the following format:
1.
Q: question_1
A: answer_1

2.
Q: question_2
A: answer_2
# and so on

Subtitles:
"""


REGEXES = [
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


def process_subtitles(subtitle_text):
    """Process subtitle text to convert it into paragraphs."""
    for pattern, repl, *flags in REGEXES:
        flags = flags[0] if flags else 0
        subtitle_text = re.sub(pattern, repl, subtitle_text, flags=flags)
    return subtitle_text.strip()


def load_and_process_file():
    """Load subtitle text from input file and process it."""
    with open(input_file, 'r', encoding='utf-8') as file:
        subtitle_text = file.read()

    # Process the subtitle text
    return process_subtitles(subtitle_text)


def generate_flashcards(processed_text):
    """Generate flashcards based on the processed text using the latest GPT model."""
    prompt = f"{prompt_static}\n\n{processed_text}"

    print(f"Sending request...")
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("api_key not available")

    client = OpenAI(
        # This is the default and can be omitted
        api_key=api_key,
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=model,
    )
    # response = openai.Completion.create(
    #     engine=model,
    #     prompt=prompt,
    #     max_tokens=500,
    #     n=1,
    #     stop=None,
    #     temperature=0.7,
    # )

    print(f"Request received")
    print(f"Choices: {len(chat_completion.choices)}")

    # Getting the pretty-printed string representation with custom settings
    pretty_response = pp.pformat(chat_completion)
    save_output(pretty_response, response_file, "Raw response")

    response = chat_completion.choices[0].message.content
    return response


def save_response(response):
    """Save the generated flashcards to the output file."""

    # Getting the pretty-printed string representation with custom settings
    pretty_data = pp.pformat(response)

    # Writing the pretty-printed string to a file
    with open(response_file, 'w', encoding='utf-8') as file:
        file.write(pretty_data)
    print(f"Raw response saved to {response_file}")


def save_output(output, output_file, output_label):
    """Save the generated output to the output file."""
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(output)
    print(f"{output_label} saved to {output_file}")


def main():
    processed_text = load_and_process_file()
    print(f"Subtitle text has been loaded and processed")
    save_output(processed_text, processed_text_file, "Processed text")
    flashcards = generate_flashcards(processed_text)
    save_output(flashcards, flashcards_file, "Flashcards")


if __name__ == "__main__":
    main()
