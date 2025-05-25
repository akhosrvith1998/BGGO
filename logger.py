import logging
import os

def setup_logger():
    """
    Sets up the logger for the bot.
    """
    logger = logging.getLogger('bot_logger')
    logger.setLevel(logging.DEBUG)  # Set to DEBUG for more detailed logs

    # Create a file handler
    log_file = 'bot.log'
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Only show INFO and higher in the console

    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.info("Logger setup completed.")
    return logger

logger = setup_logger()
