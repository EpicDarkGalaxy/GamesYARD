from dataclasses import dataclass, field
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Signal

@dataclass
class GameDetails:
    system_requirements: dict[str, str] = field(default_factory=dict)
    downloads_links: list[str] = field(default_factory=list)

@dataclass
class GameData:
    title: str
    poster_url: str
    url: str
    details: GameDetails | None = None
    poster_pixmap: QPixmap | None = None
