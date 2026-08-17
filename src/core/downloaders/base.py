from abc import ABC, abstractmethod


class BaseDownloader(ABC):
    @abstractmethod
    def can_handle(self, url: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_direct_link(self, landing_page_url: str) -> str | None:
        raise NotImplementedError
