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
        self.qa_sets_subfolder = "qa_sets"
        self.summary_file = 'summary.txt'
        self.qa_file = '_qa_set.txt'
        self.compiled_qa_file = 'qa_set_compiled.txt'
        self.qa_4_anki_file = 'qa_4_anki.txt'
        self.config_path = './config'
        self.query_for_qa = f"{self.config_path}/query_for_qa.txt"
        self.query_for_summary = f"{self.config_path}/query_for_summary.txt"

        # OpenAI configuration
        # self.model = "gpt-3.5-turbo"
        self.model = "gpt-4o-mini"
        self.api_key = os.environ.get("OPENAI_API_KEY")

        # Prompt for flashcard question-answers generation
        with open(self.query_for_qa, "r") as query_file:
            query = query_file.read()
            self.qa_prompt = query

        # Prompt for content summary
        with open(self.query_for_summary, "r") as query_file:
            query = query_file.read()
            self.summary_prompt = query

        # Validate API key
        if not self.api_key:
            raise ValueError("API key not available")
