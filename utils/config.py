import os
from dotenv import load_dotenv


class Config:
    def __init__(self):
        # Load environment variables
        load_dotenv()

        # File paths
        self.input_file = '_input_subtitles.txt'
        self.raw_input_file = 'raw_input.txt'
        self.processed_text_file = 'processed_text.txt'
        self.response_file = "response.txt"
        self.qu_sets_subfolder = "qa_sets"
        self.qa_file = '_qa_set.txt'
        self.compiled_qa_file = 'qa_set_compiled.txt'
        self.qa_4_anki_file = 'qa_4_anki.txt'

        # OpenAI configuration
        self.model = "gpt-3.5-turbo"
        self.api_key = os.environ.get("OPENAI_API_KEY")

        # Prompt for flashcard question-answers generation
        self.prompt_static = """Based on the provided subtitles from a video, which is part of an AWS Associate Developer certification preparation course, create a set of flashcard questions & answers of any item of knowledge relevant in the AWS Associate Developer exam.

Generate questions & answers in the following format:
Q: question_1
A: answer_1

Q: question_2
A: answer_2
# and so on

Subtitles:
"""

        # Validate API key
        if not self.api_key:
            raise ValueError("API key not available")
