from typing import override

from ..tools.utils import parseHtml
from .base import BaseDownloader


class MediaFireDownloader(BaseDownloader):
    def can_handle(self, url) -> bool:
        return "mediafire.com" in url

    @override
    def get_direct_link(self, landing_page_url: str) -> str | None:
        soup = parseHtml(landing_page_url)
        btn = soup.select_one("#downloadButton")
        return btn['href'] if btn else None
