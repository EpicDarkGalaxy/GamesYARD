from .akirabox import AkiraBoxDownloader
from .mediafire import MediaFireDownloader
from .filekeeper import FileKeeperDownloader



class DownloaderFactory:
    _providers = [AkiraBoxDownloader(), MediaFireDownloader(), FileKeeperDownloader()]

    @classmethod
    def get_provider(cls, url: str):
        for provider in cls._providers:
            if provider.can_handle(url):
                return provider
        return None
