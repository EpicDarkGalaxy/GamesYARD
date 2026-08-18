from abc import ABC, abstractmethod


class BaseDownloader(ABC): # Inherit from ABC

    @abstractmethod
    def can_handle(self, url: str) -> bool:
        """
        Returns True if this provider can handle the given URL.
        """
        pass # No need for 'raise NotImplementedError' anymore!

    @abstractmethod
    def get_direct_link(self, landing_page_url: str) -> str | None:
        """
        Resolves the landing page and returns the final direct file download URL.
        """
        pass
