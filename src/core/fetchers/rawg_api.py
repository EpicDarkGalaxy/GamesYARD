import re
from typing import Optional

import requests
from pydantic import BaseModel, Field
from PySide6.QtCore import QUrl

from ..models.game_data import GameData
from ..tools import get_img_data, get_logger
from .base import BaseGameFetcher

logger = get_logger(__name__)

class RequirementSpecs(BaseModel):
    os: Optional[str] = Field(None, description="Operating System requirement")
    cpu: Optional[str] = Field(None, description="Processor / CPU specifications")
    ram: Optional[str] = Field(None, description="RAM / Memory capacity")
    gpu: Optional[str] = Field(None, description="Graphics card / VRAM details")
    storage: Optional[str] = Field(None, description="Storage / disk space needed")
    directx: Optional[str] = Field(None, description="DirectX version")
    sound: Optional[str] = Field(None, description="Sound card specifications")
    network: Optional[str] = Field(None, description="Internet connection requirement")
    notes: Optional[str] = Field(None, description="Additional performance notes")
    unstructured: Optional[list[str]] = Field(
        None, description="Fallback lines if standard key-value parsing fails"
    )


class GameSystemRequirements(BaseModel):
    minimum: Optional[RequirementSpecs] = None
    recommended: Optional[RequirementSpecs] = None

SPEC_PATTERNS = {
    "os": re.compile(r"(?:OS|Operating System)\s*:\s*([^\n\r]+)", re.IGNORECASE),
    "cpu": re.compile(r"(?:Processor|CPU)\s*:\s*([^\n\r]+)", re.IGNORECASE),
    "ram": re.compile(r"(?:Memory|RAM)\s*:\s*([^\n\r]+)", re.IGNORECASE),
    "gpu": re.compile(r"(?:Graphics|Video Card|GPU)\s*:\s*([^\n\r]+)", re.IGNORECASE),
    "storage": re.compile(
        r"(?:Storage|Hard Drive(?: Space)?|Disk Space)\s*:\s*([^\n\r]+)",
        re.IGNORECASE,
    ),
    "directx": re.compile(r"(?:DirectX(?: Version)?)\s*:\s*([^\n\r]+)", re.IGNORECASE),
    "sound": re.compile(r"(?:Sound Card|Sound)\s*:\s*([^\n\r]+)", re.IGNORECASE),
    "network": re.compile(
        r"(?:Network|Broadband Internet connection)\s*:\s*([^\n\r]+)",
        re.IGNORECASE,
    ),
    "notes": re.compile(
        r"(?:Additional Notes|Notes)\s*:\s*([^\n\r]+)", re.IGNORECASE
    ),
}

class RawgApiFetcher(BaseGameFetcher):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.rawg.io/api"
        self.session = requests.session()
        
    def search_games(self, query: str, page: int = 1) -> list[GameData]:
        url  = f"{self.base_url}/games?key={self.api_key}&search={query}&page_size=15"
        params = {
            "key": self.api_key,
            "search": query,
            "page": page,
            "page_size": 15
        }

        try:
            response = self.session.get(url, timeout=5).json()
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

    @staticmethod
    def get_cropped_img_url(img_url: str) -> str:
        if not img_url:
            return ""

        target = "media/"
        if target not in img_url:
            return img_url

        # Finds where "media/" ends and inserts the crop dimensions
        index = img_url.index(target) + len(target)
        return f"{img_url[:index]}crop/600/400/{img_url[index:]}"

    def get_thumbnail(self, img_url: str, width: int = 200, height: int = 300) -> bytes | None:
        try:
            cropped_url = self.get_cropped_img_url(img_url)
            
            # Fetch the image
            response = self.session.get(img_url, timeout=5)
            
            # Raise an error if the URL returned a 404 or 500
            response.raise_for_status() 
            
            return response.content
            
        except requests.exceptions.RequestException as e:
            # FIXED: Added the missing 'f' for the f-string
            logger.error(f"Error when fetching thumb: {e}")
            return None

    def get_system_req(self, game_id):
        """Fetch and parse system requirements for a game using the RAWG API."""
        url = f"{self.base_url}/games/{game_id}?key={self.api_key}"
        try:
            response = self.session.get(url, timeout=5).json()
            platforms = response.get("platforms", [])
            # Look for PC platform data
            pc_data = next((p for p in platforms if p.get("platform", {}).get("name") == "PC"), {})

            if "requirements" in pc_data:
                return self.parse_rawg_platform_requirements(pc_data)
            return GameSystemRequirements()
        except Exception as e:
            logger.error(f"Failed to fetch system requirements for game {game_id}: {e}")
            return GameSystemRequirements()

    @staticmethod
    def parse_requirement_text(raw_text: Optional[str]) -> Optional[RequirementSpecs]:
        if not raw_text or not isinstance(raw_text, str):
            return None

        # Strip HTML tags, normalize linebreaks, and remove store headers
        cleaned = re.sub(r"<[^>]+>", "", raw_text)
        cleaned = cleaned.replace("\r\n", "\n").replace("\r", "\n")
        cleaned = re.sub(r"^(?:Minimum|Recommended):\s*", "", cleaned, flags=re.IGNORECASE).strip()

        extracted_data = {}
        for key, pattern in SPEC_PATTERNS.items():
            match = pattern.search(cleaned)
            if match:
                extracted_data[key] = match.group(1).rstrip(";,").strip()

        # Fallback to line splitting if no standard colon-separated patterns matched
        if not extracted_data:
            lines = [line.strip() for line in cleaned.split("\n") if line.strip()]
            return RequirementSpecs(unstructured=lines) if lines else None

        return RequirementSpecs(**extracted_data)

    @staticmethod
    def parse_rawg_platform_requirements(pc_platform_dict: dict) -> GameSystemRequirements:
        reqs = pc_platform_dict.get("requirements") or {}
        return GameSystemRequirements(
            minimum=parse_requirement_text(reqs.get("minimum")),
            recommended=parse_requirement_text(reqs.get("recommended")),
        )
