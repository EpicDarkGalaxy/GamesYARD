from urllib.parse import urlparse
from typing import Any, override

from src.core.services.providers.base_provider import BaseProvider


class PixelDrainProvider(BaseProvider):
    def __init__(self):
        super().__init__()

    @override
    def can_handle(self, url: str) -> bool:
        return url.startswith("https://pixeldrain.com/")

    @override
    def extract_dl_url(self, url: str) -> tuple[str, dict[str, Any] | str | None] | None:
        file_id = self._extract_file_id(url)
        if not file_id:
            return None
        dl_url = f"https://pixeldrain.com/api/file/{file_id}?download"
        return dl_url, {"filename": file_id}

    @staticmethod
    def _extract_file_id(url: str) -> str | None:
        path = urlparse(url).path.strip("/")
        parts = path.split("/")

        # Handles /u/{id}, /file/{id}, and already-direct /api/file/{id}
        if len(parts) >= 2 and parts[0] in ("u", "file"):
            return parts[1]
        if len(parts) >= 3 and parts[0] == "api" and parts[1] == "file":
            return parts[2]
        return None
