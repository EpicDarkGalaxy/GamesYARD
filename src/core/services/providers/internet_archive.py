from src.core.services.providers.base_provider import BaseProvider

class InternetArchiveProvider(BaseProvider):
    def can_handle(self, url: str) -> bool:
        return "archive.org" in url

    def extract_dl_url(self, url: str) -> tuple[str, dict] | None:
        return url, {}
