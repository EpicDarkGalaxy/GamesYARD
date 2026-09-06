from src.core.services.providers.base_provider import BaseProvider
from bs4 import BeautifulSoup
import requests


class Provider0807(BaseProvider):
	def __init__(self):
		super().__init__()
		self.headers = {
			"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
			"Accept-Language": "en-US,en;q=0.5",
			"Referer": "https://0807.st/",
		}

	def can_handle(self, url: str) -> bool:
		return "https://0807.st" in url

	def extract_dl_url(self, url: str) -> tuple[str, dict] | None:
		# Note: 0807 needs a slight adjustment to the URL format and will become
		# direct url
		return (f"{url}?dl=1", {"headers": self.headers})
