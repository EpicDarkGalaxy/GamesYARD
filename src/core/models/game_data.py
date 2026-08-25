from dataclasses import dataclass, field

from PySide6.QtCore import Signal
from PySide6.QtGui import QPixmap

@dataclass
class GameData:
    id: int
    title: str
    background_image: str | None
    released: str | None
    rating: float
    metacritic: int | None
    genres: list[str] = field(default_factory=list)
    description: str = ""
    poster_pixmap: QPixmap | None = None
    system_requirements: dict | None = None
