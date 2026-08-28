import logging

# Optional: Suppress specific noisy libraries
logging.getLogger("curl_cffi").setLevel(logging.WARNING)
logging.getLogger("PySide6").setLevel(logging.WARNING)

def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG) # Catch everything

    # File handler gets everything (DEBUG and above)
    file_handler = logging.FileHandler("app.log")
    file_handler.setLevel(logging.DEBUG)

    # Console handler only gets INFO and above (Cleaner console)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # Formatters
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
