from curl_cffi import requests
from bs4 import BeautifulSoup
from base64 import b64decode
from urllib.parse import urlparse

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def parseHtml(url):
    print(f"Testing URL: {url}\n")

    try:

        response = requests.get(
            url,
            impersonate="chrome124",
            timeout=10
        )
        if (response.status_code == 200):
            return BeautifulSoup(response.text, 'html.parser') # Returns the parsed HTML
        else:
            print("Error")
            return None
        
    except Exception as e:
        print(f"Error {e}")
        return None

def decodeBase64(url):
    path = urlparse(url).path
    encoded_part = path.split("/goto/")[-1]
    return b64decode(encoded_part).decode("utf-8")
