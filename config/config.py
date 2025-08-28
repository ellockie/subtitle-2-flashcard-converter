import os
from dotenv import load_dotenv

from config.config_base import ConfigBase


class Config(ConfigBase):
    def __init__(self):
        super().__init__()
        print(" [ Using ConfigLight ]")

        # Load environment variables
        load_dotenv()

        # File paths
        self.query_for_qa = f"{self.config_path}/query_for_qa.txt"
        self.query_for_summary = f"{self.config_path}/query_for_summary.txt"

        # OpenAI configuration
        # self.model = "gpt-3.5-turbo"
        # self.model = "gpt-4o-mini"
        self.model = "gpt-5-mini"
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
