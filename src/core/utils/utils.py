import os
import re
from base64 import b64decode
from socket import TCP_ULP
from urllib.parse import urlparse

from curl_cffi import requests
from bs4 import BeautifulSoup
from PySide6.QtGui import QColor, QIcon, QPixmap

from .log import get_logger

logger = get_logger(__name__)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def get_img_data(url: str) -> bytes:
    logger.info(f"fetching img from {url}")
    try:
        img_data = requests.get(url, timeout=8).content
        return img_data
    except Exception as e:
        logger.warning(f"failed to fetch img from {url} \nException:({e})")
        return None

def parseHtml(url) -> BeautifulSoup:
    logger.info(f"Testing url {url}")

    try:

        response = requests.get(
            url,
            timeout=10
        )
        if response.status_code == 200:
            logger.info(f"Response CODE: 200 for {url}")
            return BeautifulSoup(response.text, 'html.parser')
        else:
            logger.error(f"could not get the html for {url}")
            return BeautifulSoup("", 'html.parser')

    except Exception as e:
        logger.error(f"Error: {e}")
        return BeautifulSoup("", 'html.parser')

def decodeBase64(url) -> str:
    path = urlparse(url).path
    encoded_part = path.split("/goto/")[-1]
    return b64decode(encoded_part).decode("utf-8")

def get_site_name(url) -> str:
    domain = urlparse(url).netloc

    # Remove "www." if present
    if domain.startswith("www."):
        domain = domain[4:]
    return domain.split('.')[0]

def get_default_icon() -> QPixmap:
    pixmap = QPixmap(150,150)
    pixmap.fill(QColor("lightgray"))
    return pixmap

def get_direct_link(url: str) -> str:
    logger.info(f"fetching direct link for {url}")
    try:
        response = requests.get(url, timeout=4, impersonate="chrome124")
        soup1 = BeautifulSoup(response.text, 'html.parser')
        download_button = soup1.select_one('#downloadButton')
        if (download_button):
            logger.info(f"found direct link {download_button['href']}")
            direct_link = download_button["href"]
            return direct_link
    except Exception as e:
        logger.warning(f"failed: {e} for {url}")
        return ""

def clean_filename(filename: str):
    # Remove characters that are illegal in file names
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def download_icon(url: str) -> QIcon:
    img_data = get_img_data(url)
    if img_data:
        pixmap = QPixmap()
        pixmap.loadFromData(img_data)
        return QIcon(pixmap)
    return QIcon(get_default_icon())

def format_speed(bytes_per_sec: float) -> str:
    if bytes_per_sec < 1024:
        return f"{bytes_per_sec:.1f} B/s"
    elif bytes_per_sec < 1024 * 1024:
        return f"{bytes_per_sec / 1024:.1f} KB/s"
    else:
        return f"{bytes_per_sec / (1024 * 1024):.1f} MB/s"

def format_eta(seconds: float) -> str:
    if seconds < 60:
        return f"{seconds:.1f} seconds"
    elif seconds < 3600:
        return f"{seconds / 60:.1f} minutes"
    elif seconds < 86400:
        return f"{seconds / 3600:.1f} hours"
    else:
        return f"{seconds / 86400:.1f} days"

def get_filename_for_url(direct_url: str, headers: dict = None) -> str:
    """
    Retrieves the real filename from Content-Disposition header of the direct URL,
    falling back to the URL path.
    """
    if headers is None:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }

    try:
        # 1. Try HEAD request to inspect Content-Disposition header
        resp = requests.head(direct_url, headers=headers, impersonate="chrome124", allow_redirects=True, timeout=5)
        disposition = resp.headers.get('Content-Disposition')
        if disposition and 'filename=' in disposition:
            # Extract filename from header
            raw_filename = disposition.split('filename=')[-1].strip('"').strip("'")
            if raw_filename:
                return clean_filename(raw_filename)
    except Exception as e:
        print(f"Could not fetch filename via HEAD: {e}")

    # 2. Fallback: Parse from URL path if it looks like a filename
    parsed_path = urlparse(direct_url).path
    basename = os.path.basename(parsed_path)
    if basename and '.' in basename and not basename.startswith('d/'):
        return clean_filename(basename)

    # 3. Final Fallback
    return "game_download.zip"


def get_default_download_dir() -> str:
    # Option 1: System Downloads folder
    download_dir = os.path.join(os.path.expanduser("~"), "Downloads", "GamesYARD")

    # Option 2: Project cache/downloads folder
    # download_dir = os.path.abspath(os.path.join("cache", "downloads"))

    os.makedirs(download_dir, exist_ok=True)
    return download_dir
