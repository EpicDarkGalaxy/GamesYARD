from abc import ABC, abstractmethod

class BaseProvider(ABC):

    @abstractmethod
    def can_handle(self, url: str) -> bool:
        """
        Returns True if this provider can handle the given URL.
        """
        pass

    @abstractmethod
    def extract_dl_url(self, url: str) -> str | None:
        """
        Resolves the provider url and returns the final direct file download URL.
        """
        pass
