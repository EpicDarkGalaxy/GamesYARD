from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from ...core.models import GameData
from ..ui_signals import GameInfoWindowSignals


class GameCardWidget(QWidget):
    clicked: Signal = Signal(object)

    def __init__(self, game: GameData, on_click=None):
        super().__init__()
        if (on_click):
            self.clicked.connect(on_click)

        self.thumbnail_loaded = GameInfoWindowSignals()

        self.setObjectName("game-card")
        self.setAttribute(Qt.WA_StyledBackground, True) # Ensures QSS background is respected
        self.setFixedSize(160, 180)
        self._card = game

        # Main layout for the whole card
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setObjectName("game-card")
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # 1. The Thumbnail
        self._card_thumbnail = QLabel()
        self._card_thumbnail.setObjectName("card-thumbnail")
        self._card_thumbnail.setScaledContents(True)

        self.main_layout.addWidget(self._card_thumbnail)

        self.thumb_layout = QVBoxLayout(self._card_thumbnail)
        self.thumb_layout.setObjectName("card-thumb-layout")
        self.thumb_layout.setContentsMargins(0, 0, 0, 0)
        self.thumb_layout.setAlignment(Qt.AlignBottom)

        self.card_label = QLabel(game.title)
        self.card_label.setObjectName("card-label")
        self.card_label.setWordWrap(True)
        self.card_label.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)

        self.thumb_layout.addWidget(self.card_label)

    @property
    def thumbnail(self):
        return self._card_thumbnail.pixmap()

    @thumbnail.setter
    def thumbnail(self, pixmap: QPixmap):
        scaled_pixmap = pixmap.scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self._card_thumbnail.setPixmap(scaled_pixmap)
        self._card.poster_pixmap = scaled_pixmap
        self.thumbnail_loaded.thumbnail_loaded.emit(scaled_pixmap)

    @property
    def get_data(self):
        if (self._card):
            return self._card

    @get_data.setter
    def set_data(self, game: GameData):
        self._card = game

    def mousePressEvent(self, event):
        if (event.button() is Qt.MouseButton.LeftButton):
            self.clicked.emit(self)
            super().mousePressEvent(event)
