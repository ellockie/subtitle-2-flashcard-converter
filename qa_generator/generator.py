from openai import OpenAI
import pprint


class QAGenerator:
    def __init__(self, config, file_handler):
        self.config = config
        self.file_handler = file_handler
        self.client = OpenAI(api_key=self.config.api_key)
        # Customizing PrettyPrinter for logging
        self.pp = pprint.PrettyPrinter(indent=4, width=40, depth=2)

    def generate(self, processed_text):
        """Generate QAs based on the processed text using the latest GPT model."""
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

        qas = chat_completion.choices[0].message.content
        self.file_handler.save_output(qas, self.config.qa_file, "QAs", True)

        return qas
