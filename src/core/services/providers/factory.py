from .akirabox import AkiraBoxProvider
from .fastupload import FastUploadProvider
from .filekeeper import FileKeeperProvider
from .fileq import FileQProvider
from .mediafire import MediaFireProvider
from .pixeldrain import PixelDrainProvider

class ProviderFactory:
    def __init__(self):
        self._providers = [
            AkiraBoxProvider(),
            MediaFireProvider(),
            FileKeeperProvider(),
            FastUploadProvider(),
            FileQProvider(),
            PixelDrainProvider(),
        ]

    def get_provider(self, url: str):
        for provider in self._providers:
            if provider.can_handle(url):
                return provider
        return None
