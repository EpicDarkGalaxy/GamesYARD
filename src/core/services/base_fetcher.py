from abc import ABC, abstractmethod
from typing import List

from ..models import GameData


class BaseGameFetcher(ABC):
    @abstractmethod
    def search_games(self, query: str, page: int = 1) -> list[GameData]:
        """Search and return a list of GameData items."""
        pass

    @abstractmethod
    def get_game_details(self, game_id: str) -> dict:
        """Fetch detailed information about a specific game."""
        pass
