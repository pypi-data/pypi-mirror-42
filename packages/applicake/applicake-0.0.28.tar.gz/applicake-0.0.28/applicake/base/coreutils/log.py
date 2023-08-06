"""The applicake logger."""
import logging

class Logger:
    """The applicake logger class."""

    @staticmethod
    def create(level):
        """Create the logger."""
        logging.basicConfig(format="- %(levelname)s - %(message)s")
        logger = logging.getLogger()
        logger.setLevel(level)
        return logger
