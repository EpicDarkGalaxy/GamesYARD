from dataclasses import dataclass


@dataclass
class GameData:
    title: str
    poster_url: str
    url: str  # Game page URL
    details: 'GameDetails'
    poster_pixmap: object = None  # Assuming posterPixmap is a QPixmap or similar object


@dataclass
class GameDetails:
    system_requirements: dict[str, str]
    downloads_links: list[str]
