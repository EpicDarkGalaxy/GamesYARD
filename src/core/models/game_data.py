from dataclasses import dataclass, field
from PySide6.QtGui import QPixmap

@dataclass
class GameDetails:
    system_requirements: dict[str, str] = field(default_factory=dict)
    downloads_links: list[str] = field(default_factory=list)

@dataclass
class GameData:
    title: str
    poster_url: str
    url: str
    # Use Optional to handle the "not fetched yet" state
    details: GameDetails | None = None
    poster_pixmap: QPixmap | None = None
