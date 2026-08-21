from dataclasses import dataclass, field

from PySide6.QtCore import Signal
from PySide6.QtGui import QPixmap

@dataclass
class GameData:
    title: str
    poster_url: str
    url: str
    system_requirements: dict[str, str] = field(default_factory=dict)
    downloads_links: list[str] = field(default_factory=list)
    poster_pixmap: QPixmap | None = None
