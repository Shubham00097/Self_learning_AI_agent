import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logger(log_dir: Path, log_level: str = "INFO") -> logging.Logger:
    """
    Configure a structured size-rotated text logger for the agent.
    Ensures that log_dir exists.
    """
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
    except PermissionError as e:
        raise PermissionError(f"Cannot create log directory at {log_dir}: {e}")

    logger = logging.getLogger("agent")
    
    # Avoid duplicate handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    level = getattr(logging, log_level.upper(), logging.INFO)
    logger.setLevel(level)

    log_file = log_dir / "agent.log"
    
    # 10 MB rotation, keep 5 backups
    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    
    # We can also add a stream handler for the console
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(stream_handler)
    
    # If the instructions meant root logger, we can configure logging.getLogger()
    # but using a named logger is safer for libraries. Let's configure root as well if requested.
    root_logger = logging.getLogger()
    if not root_logger.handlers:
        root_logger.setLevel(level)
        root_logger.addHandler(file_handler)
        root_logger.addHandler(stream_handler)
        
    return logger
