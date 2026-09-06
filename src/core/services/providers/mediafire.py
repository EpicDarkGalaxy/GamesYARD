from typing_extensions import Any

from ...utils.utils import parseHtml
from .base_provider import BaseProvider


class MediaFireProvider(BaseProvider):
    def can_handle(self, url) -> bool:
        return url.startswith("https://mediafire.com/")

    def extract_dl_url(self, url: str) -> tuple[str, dict[str, Any]] | None:
        soup = parseHtml(url)
        btn = soup.select_one("#downloadButton")
        filename_elem = soup.select_one(".filename")
        if not btn:
            return None
        download_url = btn['href']
        filename = filename_elem.get_text(strip=True) if filename_elem else "download"
        return (download_url, {"filename": filename})
