from .akirabox import AkiraBoxProvider
from .fastupload import FastUploadProvider
from .filekeeper import FileKeeperProvider
from .fileq import FileQProvider
from .mediafire import MediaFireProvider
from .pixeldrain import PixelDrainProvider
from .gofile import GoFileProvider
from .datavaults import DataVaultsProvider
from .zero_eight_zero_seven import Provider0807
from .internet_archive import InternetArchiveProvider


class ProviderFactory:
    def __init__(self):
        self._providers = [
            AkiraBoxProvider(),
            MediaFireProvider(),
            FileKeeperProvider(),
            FastUploadProvider(),
            FileQProvider(),
            PixelDrainProvider(),
            GoFileProvider(),
            DataVaultsProvider(),
            Provider0807(),
            InternetArchiveProvider()
        ]

    def get_provider(self, url: str):
        for provider in self._providers:
            if provider.can_handle(url):
                return provider
        return None
