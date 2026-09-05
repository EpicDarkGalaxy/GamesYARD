import os
import re
from base64 import b64decode
from socket import TCP_ULP
from urllib.parse import urlparse

import requests
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

def get_filename_from_url(url: str) -> str:
    try:
        # 1. Try to get filename from Content-Disposition header
        # Using a HEAD request avoids downloading the whole file
        response = requests.head(url, allow_redirects=True, timeout=5)
        disposition = response.headers.get('Content-Disposition')
        if disposition and 'filename=' in disposition:
            # Extract filename from header
            return disposition.split('filename=')[-1].strip('"').strip("'")

        # 2. Fallback: Parse from URL path
        path = urlparse(url).path
        filename = path.split('/')[-1]
        if filename:
            return filename

    except Exception as e:
        print(f"Error fetching filename: {e}")

    return "game_download.zip" # Fallback

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
