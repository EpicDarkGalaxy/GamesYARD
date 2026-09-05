from curl_cffi import requests
from typing import override

from ...utils.utils import parseHtml
from .base_provider import BaseProvider


class FileQProvider(BaseProvider):
    def __init__(self):
        super().__init__()

    @override
    def can_handle(self, url: str) -> bool:
        return url.startswith("https://fileq.net/")

    @override
    def extract_dl_url(self, url: str) -> str | None:
        # 1. Fetch the landing page
        soup = parseHtml(url)

        # 2. Find the countdown element (same XFileSharing-style template as FileKeeper)
        countdown_element = soup.select_one("#download-countdown")
        if not countdown_element:
            return None

        # 3. Extract the variables from the data attributes
        code = countdown_element.get("data-code")
        referer = countdown_element.get("data-referer", "")
        rand = countdown_element.get("data-rand")
        method = countdown_element.get("data-method", "Free download")

        # 4. Prepare the POST payload to trigger the download unlock
        payload = {
            "op": "download2",
            "id": code,
            "rand": rand,
            "referer": referer,
            "method_free": method,
            "down_direct": "1",
        }

        # 5. POST to the same URL, keeping session/cookies intact
        post_response = requests.post(
            url, data=payload, impersonate="chrome124", stream=True
        )
        post_response.close()
        return post_response.url
