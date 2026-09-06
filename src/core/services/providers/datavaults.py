from bs4 import BeautifulSoup
from curl_cffi import requests
from typing import override

from src.core.services.providers.base_provider import BaseProvider
from src.core.utils.utils import clean_filename


class DataVaultsProvider(BaseProvider):
	def __init__(self) -> None:
		super().__init__()

	@override
	def can_handle(self, url: str) -> bool:
		return "datavaults.co" in url

	@override
	def extract_dl_url(self, url: str) -> tuple[str, dict] | None:
		# Since Datavaults uses multi-step landing pages + countdowns + reCAPTCHA,
		# we immediately hand it over to the embedded browser dialog where the user
		# can click "Click to Download", wait the countdown, and solve the reCAPTCHA.
		return ("CAPTCHA_REQUIRED", {"url": url})
