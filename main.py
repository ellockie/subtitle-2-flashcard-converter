from subtitle_processor.processor import SubtitleProcessor
from flashcard_generator.generator import FlashcardGenerator
from utils.file_handler import FileHandler
from utils.config import Config


def main():
    # Initialize configuration
    config = Config()

    # Initialize file handler for input/output operations
    file_handler = FileHandler(config)

    # Process subtitles
    subtitle_processor = SubtitleProcessor(config, file_handler)
    processed_text = subtitle_processor.process()
    print(f"Subtitle text has been loaded and processed")

    # Generate flashcards
    flashcard_generator = FlashcardGenerator(config, file_handler)
    flashcards = flashcard_generator.generate(processed_text)

    # Optionally add a description to the output folder
    # file_handler.add_description("some_description")


if __name__ == "__main__":
    main()
