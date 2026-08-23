from bs4 import BeautifulSoup
from curl_cffi import requests
from .base import BaseDownloader

class AkiraBoxDownloader(BaseDownloader):
    def can_handle(self, url: str) -> bool:
        return "akirabox.to" in url

    def get_method(self) -> object:
        return self.extract_dl_url

    def extract_dl_url(self, provider_url: str) -> str | None:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Referer": "https://akirabox.to/",
        }

        try:
            # Using curl_cffi with impersonation to bypass basic bot detection
            response = requests.get(provider_url, headers=headers, impersonate="chrome124", timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            button = soup.select_one("#download-button")

            if button and button.has_attr('href'):
                return button['href']
            return None

        except Exception as e:
            print(f"AkiraBox error: {e}")
            return None
