from base64 import b64decode
from urllib.parse import urlparse


def decodeBase64(url: str) -> str:
    path = urlparse(url).path
    encoded_part = path.split("/goto/")[-1]
    return b64decode(encoded_part).decode("utf-8")


def get_site_name(url: str) -> str:
    domain = urlparse(url).netloc

    # Remove "www." if present
    if domain.startswith("www."):
        domain = domain[4:]
    return domain.split('.')[0]
