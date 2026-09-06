from abc import ABC, abstractmethod
from typing import Any

class BaseProvider(ABC):

    @abstractmethod
    def can_handle(self, url: str) -> bool:
        """
        Returns True if this provider can handle the given URL.
        """
        raise NotImplementedError

    @abstractmethod
    def extract_dl_url(self, url: str) -> tuple[str, dict] | None:
        """
        Resolves the provider url and returns the final direct file download URL.
        """
        raise NotImplementedError
