from openai import OpenAI
import pprint
from utils.file_handler import FileHandler

class FlashcardGenerator:
    def __init__(self, config):
        self.config = config
        self.client = OpenAI(api_key=self.config.api_key)
        # Customizing PrettyPrinter for logging
        self.pp = pprint.PrettyPrinter(indent=4, width=40, depth=2)
        self.file_handler = FileHandler(config)

    def generate(self, processed_text):
        """Generate flashcards based on the processed text using the latest GPT model."""
        prompt = f"{self.config.prompt_static}\n\n{processed_text}"

        print(f"Sending request...")
        chat_completion = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.config.model,
        )

        print(f"Request received")
        print(f"Choices: {len(chat_completion.choices)}")

        # Log the raw response
        pretty_response = self.pp.pformat(chat_completion)
        self.file_handler.save_output(pretty_response, self.config.response_file, "Raw response")

        return chat_completion.choices[0].message.content
