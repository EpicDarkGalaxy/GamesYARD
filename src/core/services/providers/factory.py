from .akirabox import AkiraBoxProvider
from .mediafire import MediaFireProvider
from .filekeeper import FileKeeperProvider



class ProviderFactory:
    _providers = [AkiraBoxProvider(), MediaFireProvider(), FileKeeperProvider()]

    @classmethod
    def get_provider(cls, url: str):
        for provider in cls._providers:
            if provider.can_handle(url):
                return provider
        return None
