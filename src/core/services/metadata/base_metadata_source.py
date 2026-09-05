# src/core/services/metadata/base_metadata_source.py
from abc import ABC, abstractmethod

from src.core.models import GameData


class BaseMetadataSource(ABC):
    @abstractmethod
    def search_games(self, query: str, page: int = 1) -> list[GameData]:
        """Search for games matching a query string."""
        ...

    @abstractmethod
    def get_home_catalog(self) -> dict[str, list[GameData]]:
        """Returns curated sections (featured, trending, newest, best_rated, etc.)."""
        ...

    @abstractmethod
    def get_thumbnail(self, img_url: str) -> bytes | None:
        """Fetches raw image bytes for a given thumbnail/poster URL."""
        ...

    @abstractmethod
    def get_game_screenshots(self, game_id: str) -> list[bytes]:
        """Returns a list of screenshot image bytes for a game."""
        ...

    @abstractmethod
    def get_game_system_requirements(self, game_id: str) -> dict:
        """Returns structured PC system requirements for a game."""
        ...
