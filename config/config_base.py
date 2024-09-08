class ConfigBase:
    def __init__(self):
        print(" [ ConfigBase ]")

        # File paths
        self.input_file = "_input_subtitles.txt"
        self.raw_input_file = "raw_input.txt"
        self.processed_text_file = "processed_text.txt"
        self.response_file = "response.txt"
        self.qa_sets_subfolder = "qa_sets"
        self.summary_file = "summary.txt"
        self.qa_file = "_qa_set.txt"
        self.compiled_qa_file = "qa_set_compiled.txt"
        self.qa_4_anki_file = "qa_4_anki.txt"
        self.config_path = "./config"
        self.video_name = None
