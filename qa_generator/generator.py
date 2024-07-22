from openai import OpenAI
import pprint

from constants.constants import OUTPUT_TYPE


class QAGenerator:
    def __init__(self, config, file_handler):
        self.config = config
        self.file_handler = file_handler
        self.client = OpenAI(api_key=self.config.api_key)
        # Customizing PrettyPrinter for logging
        self.pp = pprint.PrettyPrinter(indent=4, width=40, depth=2)

    def generate(self, processed_text, generate_summary=False):
        """Generate QAs or summary based on the processed text using the latest GPT model."""
        if generate_summary:
            prompt = f"{self.config.summary_prompt}\n\n{processed_text}"
            output_file = self.config.summary_file
            output_type = OUTPUT_TYPE["Summary"]
        else:
            prompt = f"{self.config.qa_prompt}\n\n{processed_text}"
            output_file = self.config.qa_file
            output_type = OUTPUT_TYPE["QAs"]

        print(f"Sending request for {output_type}...")
        chat_completion = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.config.model,
        )

        print(f"Request received")
        print(f"Choices: {len(chat_completion.choices)}")

        # Log the raw response
        pretty_response = self.pp.pformat(chat_completion)
        self.file_handler.save_output(pretty_response, self.config.response_file, f"Raw response for {output_type}")

        generated_content = chat_completion.choices[0].message.content
        self.file_handler.save_output(generated_content, output_file, output_type)

        return generated_content
