from ...utils.utils import parseHtml
from .base import BaseProvider


class MediaFireProvider(BaseProvider):
    def can_handle(self, url) -> bool:
        return "mediafire.com" in url

    def extract_dl_url(self, provider_url: str) -> str | None:
        soup = parseHtml(provider_url)
        btn = soup.select_one("#downloadButton")
        return btn['href'] if btn else None
