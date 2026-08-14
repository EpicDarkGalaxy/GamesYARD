from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QLabel, QStyle, QStyleOption, QVBoxLayout, QWidget

from ...core.models import GameData


class GameCardWidget(QWidget):
    clicked = Signal(object)

    def __init__(self, game: GameData, on_click=None):
        super().__init__()
        if (on_click):
            self.clicked.connect(on_click)

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
        self.card_thumbnail = QLabel()
        self.card_thumbnail.setObjectName("card-thumbnail")
        self.card_thumbnail.setScaledContents(True)

        self.main_layout.addWidget(self.card_thumbnail)

        self.thumb_layout = QVBoxLayout(self.card_thumbnail)
        self.thumb_layout.setObjectName("card-thumb-layout")
        self.thumb_layout.setContentsMargins(0, 0, 0, 0)
        self.thumb_layout.setAlignment(Qt.AlignBottom)

        self.card_label = QLabel(game.title)
        self.card_label.setObjectName("card-label")
        self.card_label.setWordWrap(True)
        self.card_label.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)

        self.thumb_layout.addWidget(self.card_label)

    @property
    def get_data(self):
        if (self._card):
            return self._card

    def mousePressEvent(self, event):
        if (event.button() is Qt.MouseButton.LeftButton):
            self.clicked.emit(self)
        super().mousePressEvent(event)
