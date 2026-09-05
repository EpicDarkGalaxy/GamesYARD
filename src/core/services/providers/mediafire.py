from ...utils.utils import parseHtml
from .base_provider import BaseProvider


class MediaFireProvider(BaseProvider):
    def can_handle(self, url) -> bool:
        return url.startswith("https://mediafire.com/")

    def extract_dl_url(self, url: str) -> str | None:
        soup = parseHtml(url)
        btn = soup.select_one("#downloadButton")
        return btn['href'] if btn else None
