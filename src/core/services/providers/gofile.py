import hashlib
import time
from typing import override

from curl_cffi import requests

from src.core.services.providers.base_provider import BaseProvider
from src.core.utils import get_logger
from typing import Any

logger = get_logger(__name__)


class GoFileProvider(BaseProvider):
	def __init__(self) -> None:
		super().__init__()

	@override
	def can_handle(self, url: str) -> bool:
		return "https://gofile.io" in url

	@override
	def extract_dl_url(self, url: str) -> tuple[str, dict[str, Any]] | None:
		user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"

		# Step 1: Create a guest account session if no token exists
		session = requests.Session()

		# Generate initial token
		wt = self.generate_gofile_website_token(user_agent=user_agent, account_token="")

		headers = {
			"User-Agent": user_agent,
			"X-Website-Token": wt,
			"X-BL": "en-US",
			"Accept": "*/*"
		}

		# Fetch a guest account token from GoFile
		account_resp = session.post("https://api.gofile.io/accounts", headers=headers)

		if account_resp.status_code == 200:
			account_data = account_resp.json()
			account_token = account_data.get("data", {}).get("token", "")
			print(f"Acquired Account Token: {account_token}")

			# Step 2: Regenerate website token with the account token
			updated_wt = self.generate_gofile_website_token(user_agent=user_agent, account_token=account_token)

			# Now make an API call to get folder/file information
			folder_id = url.split("/")[-1]  # e.g., the ID from https://gofile.io/d/FOLDER_ID

			api_headers = {
				"User-Agent": user_agent,
				"Authorization": f"Bearer {account_token}",
				"X-Website-Token": updated_wt,
				"X-BL": "en-US"
			}

			download_headers = {
	            "User-Agent": user_agent,
	            "Authorization": f"Bearer {account_token}",
	            "Cookie": f"accountToken={account_token}",
	            "Referer": "https://gofile.io/",
	            "Accept": "*/*"
        	}

			content_json = session.get(f"https://api.gofile.io/contents/{folder_id}", headers=api_headers).json()
			logger.debug(f"Content JSON: {content_json}")
			data: dict[str, Any] = content_json.get("data", {})
			children = data.get("children", {})
			if children:
				for value in children.values():
					if isinstance(value, dict):
						link = value.get("link")
						filename = value.get("name")
						if link:
							return link, {"filename": filename, "headers": download_headers}
		return None


	@staticmethod
	def generate_gofile_website_token(user_agent: str, account_token: str = "") -> str:
		"""
		Generates the X-Website-Token for GoFile requests.

		:param user_agent: The exact User-Agent string sent with requests.
		:param account_token: Account token or guest token (leave empty if unauthenticated).
		:param language: Default language string passed in X-BL header.
		"""
		# GoFile updates the token every 4 hours (14400 seconds)
		time_slot = int(time.time()) // 14400

		# GoFile salt value (hardcoded in frontend scripts like alljs.js / wt.obf.js)
		salt = "12af056dacea0b"

		# Format: {user_agent}::{language}::{account_token}::{time_slot}::{salt}
		raw_str = f"{user_agent}::en-US::{account_token}::{time_slot}::{salt}"

		return hashlib.sha256(raw_str.encode("utf-8")).hexdigest()
