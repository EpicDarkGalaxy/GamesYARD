from curl_cffi import requests
from .base import BaseGameFetcher
from ..models.game_data import GameData
from ..tools.log import get_logger

logger = get_logger(__name__)

class RawgApiFetcher(BaseGameFetcher):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.rawg.io/api"

    def search_games(self, query: str, page: int = 1) -> list[GameData]:
        url  = f"{self.base_url}/games?key={self.api_key}&search={query}&page_size=15"
        params = {
            "key": self.api_key,
            "search": query,
            "page": page,
            "page_size": 15
        }

        try:
            response = requests.get(url).json()
            results = response.get("results", [])

            games = []
            for item in results:
                games.append(GameData(
                    id=item.get("id"),
                    title=item.get("name"),
                    background_image=item.get("background_image"),
                    released=item.get("released"),
                    rating=item.get("rating", 0.0),
                    metacritic=item.get("metacritic"),
                    genres=[g.get("name") for g in item.get("genres", [])],
                    description=""  # Populated when detail view is called
                ))
                logger.info(f"Successfully fetched {len(games)} games for query: {query}")
            return games
        except Exception:
            logger.error("Failed to fetch games from RAWG API")
            return []

    def get_game_details(self, game_id: str) -> dict:
        """Fetch detailed information about a specific game."""
        pass

    def get_system_requirements(self, game_id: str) -> dict:
        url = f"{self.base_url}/games/{game_id}"
        params = {"key": self.api_key}
        data = requests.get(url, params=params).json()

        requirements = {"minimum": "Not specified", "recommended": "Not specified"}

        # Iterate through platforms to find the PC entry
        for platform_info in data.get("platforms", []):
            if platform_info["platform"]["name"].lower() == "pc":
                reqs = platform_info.get("requirements", {})
                requirements["minimum"] = reqs.get("minimum", "Not specified")
                requirements["recommended"] = reqs.get("recommended", "Not specified")
                break

        return requirements
