import logging
import os
from .config import LOG_FILE, LOG_LEVEL

def get_logger(name):
    """
    Creates and returns a configured logger instance.
    Logs to both console and a file defined in config.py.
    """
    logger = logging.getLogger(name)
    
    # Avoid adding multiple handlers to the same logger
    if not logger.handlers:
        level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
        logger.setLevel(level)

        # Create handlers
        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler(LOG_FILE)
        
        c_handler.setLevel(level)
        f_handler.setLevel(level)

        # Create formatter and add it to handlers
        c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)

        # Add handlers to the logger
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)

    return logger
