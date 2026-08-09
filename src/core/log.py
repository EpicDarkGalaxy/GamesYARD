import logging


class LevelFilter(logging.Filter):
    def __init__(self, level):
        self.level = level

    def filter(self, record):
        return record.levelno <= self.level

logging.basicConfig(
    level=logging.INFO,  # Changed from DEBUG to INFO to suppress DEBUG logs
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(),
    ]
)

# Optional: Suppress specific noisy libraries
logging.getLogger("curl_cffi").setLevel(logging.WARNING)
logging.getLogger("PySide6").setLevel(logging.WARNING)

def get_logger(name: str):
    return logging.getLogger(name)
