import logging

class DeploymentLogger:
    def __init__(self):
        """Initialize the logger with basic configuration"""
        self.logger = logging.getLogger("DeploymentLogger")
        self.logger.setLevel(logging.INFO)

        # Console handler
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        self.logger.addHandler(handler)

    def log_info(self, message):
        """Log general info messages."""
        self.logger.info(message)

    def log_error(self, message):
        """Log error messages before raising exceptions."""
        self.logger.error(message)

    def log_debug(self, message):
        """Log debug information (optional for development)."""
        self.logger.debug(message)
