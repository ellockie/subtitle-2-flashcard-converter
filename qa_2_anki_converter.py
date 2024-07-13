import os
import re
import sys

from utils.config import Config


def convert_qas_to_anki(input_path):
    """
    Convert QAs from the original format to Anki format.

    :param input_path: Path to the folder containing a compiled version of QAs file (manually compiled)
    """
    input_file = os.path.join(input_path, Config.compiled_qa_file)
    output_file = os.path.join(input_path, Config.qa_4_anki_file)

    if not os.path.exists(input_file):
        print(f"Error: '{Config.compiled_qa_file}' not found in {input_path}")
        return

    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        content = infile.read()

        # Use regex to find all Q&A pairs
        qa_pairs = re.findall(r'Q: (.*?)\nA: (.*?)(?=\n\d+\.|\Z)', content, re.DOTALL)

        for question, answer in qa_pairs:
            # Clean up the question and answer
            question = question.strip().replace('"', '""')
            answer = answer.strip().replace('"', '""')

            # Write in Anki format
            outfile.write(f'"{question}";"{answer}"\n')

    print(f"Conversion complete. Anki-ready QAs saved to {output_file}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python qa_2_anki_converter.py <path_to_folder>")
        sys.exit(1)

    folder_path = sys.argv[1]
    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} is not a valid directory")
        sys.exit(1)

    convert_qas_to_anki(folder_path)
