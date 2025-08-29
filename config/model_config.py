import os
from dotenv import load_dotenv

class ModelConfig:
    def __init__(self):
        load_dotenv()
        # Model configuration
        # self.model = "gpt-3.5-turbo"
        # self.model = "gpt-4o-mini"
        self.model = "gpt-5-mini"
        self.api_key = os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("API key not available")
