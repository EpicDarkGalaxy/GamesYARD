from src.core.services.providers.base_provider import BaseProvider
from src.core.utils.utils import parseHtml


class FastUploadProvider(BaseProvider):
    def __init__(self):
        super().__init__()

    def can_handle(self, url: str) -> bool:
        return url.startswith("https://fastupload.io/")

    def extract_dl_url(self, url: str) -> str | None:
        soup = parseHtml(url)

        form = soup.find("form")
        if form is None:
            return None

        action = form.get("action")
        if not action:
            return None

        return action
