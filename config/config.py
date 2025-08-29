from dotenv import load_dotenv
from config.config_base import ConfigBase
from config.model_config import ModelConfig
from config.prompts.prompt_config import (
    PROMPTS_FOLDER,
    PROMPT_FOR_QA_FILENAME,
    PROMPT_FOR_SUMMARY_FILENAME,
)


class Config(ConfigBase):
    def __init__(self):
        super().__init__()
        print(" [ Using ConfigLight ]")

        # Load environment variables
        load_dotenv()

        # File paths
        self.prompt_for_qa = f"{PROMPTS_FOLDER}/{PROMPT_FOR_QA_FILENAME}"
        self.prompt_for_summary = f"{PROMPTS_FOLDER}/{PROMPT_FOR_SUMMARY_FILENAME}"

        # Model configuration
        model_config = ModelConfig()
        self.model = model_config.model
        self.api_key = model_config.api_key

        # Prompt for flashcard question-answers generation
        with open(self.prompt_for_qa, "r") as prompt_file:
            prompt = prompt_file.read()
            self.qa_prompt = prompt

        # Prompt for content summary
        with open(self.prompt_for_summary, "r") as prompt_file:
            prompt = prompt_file.read()
            self.summary_prompt = prompt

        # Validate API key
        if not self.api_key:
            raise ValueError("API key not available")
