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
    subtitle_processor = SubtitleProcessor(config)
    processed_text = subtitle_processor.process()
    print(f"Subtitle text has been loaded and processed")
    file_handler.save_output(processed_text, config.processed_text_file, "Processed text")

    # Generate flashcards
    flashcard_generator = FlashcardGenerator(config)
    flashcards = flashcard_generator.generate(processed_text)
    file_handler.save_output(flashcards, config.flashcards_file, "Flashcards")


if __name__ == "__main__":
    main()
