import os
import requests
from PySide6.QtGui import QPixmap, QIcon

CACHE_DIR = "cache/assets"
os.makedirs(CACHE_DIR, exist_ok=True)

def get_asset(url: str, filename: str = "") -> str:
    """
    Downloads an asset (like an icon or badge) to a local cache folder.
    Returns the absolute path to the local file.
    """
    if not filename:
        # Generate a safe filename if none provided
        filename = os.path.basename(url)

    local_path = os.path.join(CACHE_DIR, filename)

    # 1. Return cached file if it exists
    if os.path.exists(local_path):
        return local_path

    # 2. Download if not in cache
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            with open(local_path, 'wb') as f:
                f.write(response.content)
            return local_path
    except Exception as e:
        print(f"Failed to download asset {url}: {e}")

    return ""

def get_icon_from_url(url: str) -> QIcon:
    """Helper to get a QIcon directly from a remote URL."""
    path = get_asset(url)
    return QIcon(path) if path else QIcon()
