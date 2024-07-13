from subtitle_processor.processor import SubtitleProcessor
from qa_generator.generator import QAGenerator
from utils.file_handler import FileHandler
from utils.config import Config
from utils.print_stats import count_qa_sets


def main():
    # Initialize configuration
    config = Config()

    # Initialize file handler for input/output operations
    file_handler = FileHandler(config)

    # Create plain text from subtitles
    SP = SubtitleProcessor(config, file_handler)
    plain_text = SP.get_plain_text_from_subtitles()
    print(f"Subtitle text has been loaded and processed into plain text")

    # Generate QAs
    QAG = QAGenerator(config, file_handler)
    qas = QAG.generate(plain_text)

    # Print stats
    count_qa_sets(qas)

    # Optionally add a description to the output folder
    # file_handler.add_description("some_description")


if __name__ == "__main__":
    main()
