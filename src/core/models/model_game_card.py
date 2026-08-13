from dataclasses import dataclass
from typing import Optional


@dataclass
class GameCard:
    title: str
    poster_url: str
    url: str  # Game page URL
    details: Optional['GameDetails'] = None
    poster_pixmap: object = None  # Assuming posterPixmap is a QPixmap or similar object


@dataclass
class GameDetails:
    system_requirements: dict[str, str]
    downloads_links: list[str]
