import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("app.log"),  # Output logs to a file
        logging.StreamHandler(),  # Output logs to the console
    ]
)

logger = {}

def get_logger(name: str):
    return logging.getLogger(name)