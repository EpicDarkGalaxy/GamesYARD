import os
import re
from base64 import b64decode
from urllib.parse import unquote, urlparse

from bs4 import BeautifulSoup
from curl_cffi import requests
from PySide6.QtGui import QColor, QPixmap

from .log import get_logger

logger = get_logger(__name__)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def get_img_data(url: str) -> bytes:
    logger.info(f"fetching img from {url}")
    try:
        img_data = requests.get(url, timeout=4).content
        return img_data
    except Exception as e:
        logger.warning("failed to fetch img")
        return None

def parseHtml(url) -> BeautifulSoup:
    logger.info(f"Testing url {url}")

    try:

        response = requests.get(
            url,
            impersonate="chrome124",
            timeout=10
        )
        if response.status_code == 200:
            logger.info("Response CODE: 200")
            return BeautifulSoup(response.text, 'html.parser')
        else:
            logger.error("could not get the html")
            return BeautifulSoup("", 'html.parser')

    except Exception as e:
        logger.error("No Internet I guess (:")
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
        logger.warning(f"failed to fetch direct link for {url}")
        return ""

def clean_filename(filename):
    # Remove characters that are illegal in file names
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def get_filename_from_url(url: str) -> str:
    # 1. Parse the URL
    parsed = urlparse(url)
    path = parsed.path  # Result: "/file/pq2gf5st6u8ajxb/PVZGOTY2009.rar/file"

    # 2. Split into parts: ['', 'file', 'pq2gf5st6u8ajxb', 'PVZGOTY2009.rar', 'file']
    parts = path.split('/')

    # 3. Look for the part that ends in a known extension
    extensions = ('.rar', '.zip', '.7z', '.exe', '.msi')
    for part in parts:
        if part.lower().endswith(extensions):
            return part

    # 4. Fallback if no extension found
    return "downloaded_file"
