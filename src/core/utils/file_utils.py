import os
import sys


def clean_filename(filename: str) -> str:
    """Remove characters that are illegal in file names."""
    return filename.replace('\x00', '')


def get_default_download_dir() -> str:
    """Return a default download directory and ensure it exists."""
    download_dir = os.path.join(os.path.expanduser("~"), "Downloads", "GamesYARD")
    os.makedirs(download_dir, exist_ok=True)
    return download_dir


def resource_path(relative_path: str) -> str:
    """Get absolute path to resource, works for dev and for PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
