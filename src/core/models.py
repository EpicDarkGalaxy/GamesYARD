from dataclasses import dataclass

@dataclass
class GameCardData:
    title: str
    href: str
    posterLink: str
    posterPixmap: object  # Assuming posterPixmap is a QPixmap or similar object
    downloads_links: list

@dataclass
class GameDetails(GameCardData):
    system_requirements: dict