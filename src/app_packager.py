class AppPackager:
    def __init__(self, source_dir, output_dir, logger):
        self.source_dir = source_dir
        self.output_dir = output_dir
        self.logger = logger

    def create_package(self):
        """Stub method for packaging."""
        return f"{self.output_dir}/app.zip"
