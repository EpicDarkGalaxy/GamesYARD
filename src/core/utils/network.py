from curl_cffi import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os
import re
from typing import Optional

from .log import get_logger

logger = get_logger(__name__)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def get_img_data(url: str) -> Optional[bytes]:
    """Fetch image bytes from a URL. Returns None on failure."""
    logger.info(f"fetching img from {url}")
    try:
        img_data = requests.get(url, timeout=8).content
        return img_data
    except Exception as e:
        logger.warning(f"failed to fetch img from {url} \nException:({e})")
        return None


def parseHtml(url: str) -> BeautifulSoup:
    logger.info(f"Testing url {url}")

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            logger.info(f"Response CODE: 200 for {url}")
            return BeautifulSoup(response.text, 'html.parser')
        else:
            logger.error(f"could not get the html for {url}")
            return BeautifulSoup("", 'html.parser')

    except Exception as e:
        logger.error(f"Error: {e}")
        return BeautifulSoup("", 'html.parser')


def get_direct_link(url: str) -> str:
    logger.info(f"fetching direct link for {url}")
    try:
        response = requests.get(url, timeout=4, impersonate="chrome124")
        soup1 = BeautifulSoup(response.text, 'html.parser')
        download_button = soup1.select_one('#downloadButton')
        if download_button:
            logger.info(f"found direct link {download_button['href']}")
            return download_button["href"]
    except Exception as e:
        logger.warning(f"failed: {e} for {url}")
    return ""


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
                return re.sub(r'[\\/*?:"<>|]', "", raw_filename)
    except Exception as e:
        logger.warning(f"Could not fetch filename via HEAD: {e}")

    # 2. Fallback: Parse from URL path if it looks like a filename
    parsed_path = urlparse(direct_url).path
    basename = os.path.basename(parsed_path)
    if basename and '.' in basename and not basename.startswith('d/'):
        return re.sub(r'[\\/*?:"<>|]', "", basename)

    # 3. Final Fallback
    return "game_download.zip"
