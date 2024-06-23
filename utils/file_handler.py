class FileHandler:
    def __init__(self, config):
        self.config = config

    def save_output(self, output, output_file, output_label):
        """Save the generated output to the specified output file."""
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(output)
        print(f"{output_label} saved to {output_file}")
