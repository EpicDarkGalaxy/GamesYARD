import re
from typing import Optional

import requests
from pydantic import BaseModel, Field
from PySide6.QtCore import QUrl

from ..models.game import GameData
from ..utils import get_img_data, get_logger
from .base_fetcher import BaseGameFetcher

logger = get_logger(__name__)

class RawgAPI(BaseGameFetcher):
    def __init__(self, api_key: str):
        self.api_key = api_key
        if not api_key:
            logger.warning("RAWG API key was not given")

        self.base_url = "https://api.rawg.io/api"
        self.session = requests.session()

    def search_games(self, query: str, page: int = 1) -> list[GameData]:
        url = f"{self.base_url}/games"
        params = {
            "key": self.api_key,
            "search": query,
            "page": page,
            "page_size": 15
        }

        try:
            response = self.session.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            results: list[dict] = data.get("results", [])

            games: list[GameData] = []
            for item in results:
                games.append(GameData(
                    id=item.get("id"),
                    title=item.get("name"),
                    background_image=item.get("background_image"),
                    released=item.get("released"),
                    rating=item.get("rating", 0.0),
                    metacritic=item.get("metacritic"),
                    genres=[g.get("name") for g in item.get("genres", []) if isinstance(g, dict)],
                    description="",  # Populated when detail view is called
                ))
            logger.info(f"Successfully fetched {len(games)} games for query: {query}")
            return games
        except requests.RequestException as e:
            logger.error(f"Failed to fetch games from RAWG API: {e}")
            return []

    def get_game_details(self, game_id: str) -> dict:
        """Fetch detailed information about a specific game."""
        pass

    def get_thumbnail(self, img_url: str) -> bytes | None:
        try:
            logger.info(f"Fetching thumbnail for URL: {img_url}")

            # Fetch the image
            response = self.session.get(img_url, timeout=5)

            # Raise an error if the URL returned a 404 or 500
            response.raise_for_status()

            return response.content

        except requests.exceptions.RequestException as e:
            logger.error(f"Error when fetching thumb: {e}")
            return None

    def get_game_screenshots(self, game_id: str) -> list[bytes]:
        """
        Returns a list of bytes for official game screenshots.
        """
        url = f"{self.base_url}/games/{game_id}/screenshots"
        params = {"key": self.api_key}

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            results = data.get("results", [])

            screenshot_bytes = []
            for item in results:
                image_url = item.get("image")
                if image_url:
                    img_response = self.session.get(image_url, timeout=5)
                    img_response.raise_for_status()
                    screenshot_bytes.append(img_response.content)

            return screenshot_bytes
        except requests.RequestException as e:
            logger.error(f"Error fetching screenshots: {e}")
            return []


    def parse_requirements_text(self, raw_text: str) -> dict:
        """Extracts specs from RAWG's unformatted requirement text block."""
        if not raw_text:
            return {"Not Specified": "Not Specified"}

        # Key specs to extract using regex lookaheads for next fields
        field_patterns = {
            "OS": r"(?:OS|Operating System)\s*:\s*(.*?)(?=\s*(?:Processor|Memory|Graphics|DirectX|Storage|Sound Card|Network|Additional Notes)|$)",
            "CPU": r"(?:Processor|CPU)\s*:\s*(.*?)(?=\s*(?:OS|Memory|Graphics|DirectX|Storage|Sound Card|Network|Additional Notes)|$)",
            "RAM": r"(?:Memory|RAM)\s*:\s*(.*?)(?=\s*(?:OS|Processor|Graphics|DirectX|Storage|Sound Card|Network|Additional Notes)|$)",
            "GPU": r"(?:Graphics|Video Card|GPU)\s*:\s*(.*?)(?=\s*(?:OS|Processor|Memory|DirectX|Storage|Sound Card|Network|Additional Notes)|$)",
            "DirectX": r"(?:DirectX)\s*:\s*(.*?)(?=\s*(?:OS|Processor|Memory|Graphics|Storage|Sound Card|Network|Additional Notes)|$)",
            "Storage": r"(?:Storage|Hard Drive|Hard Disk Space)\s*:\s*(.*?)(?=\s*(?:OS|Processor|Memory|Graphics|DirectX|Sound Card|Network|Additional Notes)|$)",
        }

        structured_specs = {}

        for spec_key, pattern in field_patterns.items():
            match = re.search(pattern, raw_text, re.IGNORECASE | re.DOTALL)
            if match:
                # Clean up newlines and trailing whitespace
                val = match.group(1).strip()
                # Take only the relevant line if multi-line text bled over
                val = val.split("\n")[0].strip()
                structured_specs[spec_key] = val

        return structured_specs

    def get_game_system_requirements(self, game_id: str) -> dict:
        """Queries RAWG API and structures the PC requirements for a specific game."""
        logger.info(f"Initiating system requirements fetch for game_id: {game_id}")
        game_data = {}
        try:
            url = f"{self.base_url}/games/{game_id}?key={self.api_key}"
            response = self.session.get(url, timeout=5)
            response.raise_for_status()
            game_data = response.json()
        except Exception as e:
            logger.error(f"Failed to fetch system requirements for {game_id}: {e}")
            return {}

        # Find PC platform entry
        pc_requirements = {}
        for platform_info in game_data.get("platforms", []):
            if platform_info.get("platform", {}).get("slug") == "pc":
                pc_requirements = platform_info.get("requirements", {}) or {}
                break

        raw_min = pc_requirements.get("minimum", "")
        raw_rec = pc_requirements.get("recommended", "")

        logger.info(f"Successfully processed system requirements for: {game_data.get('name')}")
        logger.debug(f"Minimun: {raw_min} \nRecommended: {raw_rec}")

        return {
            "id": game_data.get("id"),
            "game": game_data.get("name"),
            "slug": game_data.get("slug"),
            "requirements": {
                "minimum": self.parse_requirements_text(raw_min),
                "recommended": self.parse_requirements_text(raw_rec),
            },
        }
