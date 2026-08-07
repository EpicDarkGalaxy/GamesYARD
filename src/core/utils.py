from curl_cffi import Request as requests
from bs4 import BeautifulSoup
from base64 import b64decode
from urllib.parse import urlparse

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def get_img_data(url: str):
    try:
        img_data = requests.get(url, timeout=4).content
        return img_data
    except Exception as e:
        return None
    
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
            return []
        
    except Exception as e:
        return []

def decodeBase64(url):
    path = urlparse(url).path
    encoded_part = path.split("/goto/")[-1]
    return b64decode(encoded_part).decode("utf-8")
