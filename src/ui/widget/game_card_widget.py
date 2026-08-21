from PySide6.QtCore import QRectF, Qt, Signal, Slot
from PySide6.QtGui import QIcon, QPainter, QPainterPath, QPixmap, QRegion
from PySide6.QtWidgets import QFrame, QLabel, QSizePolicy, QVBoxLayout
from uuid import uuid4
from ...core.models import GameData


class GameCard(QFrame):
    request_card: Signal = Signal(object)
    thumb_loaded: Signal = Signal(QPixmap)

    def __init__(self, game: GameData, on_click=None):
        super().__init__()
        self._id = str(uuid4())
        if (on_click):
            self.request_card.connect(on_click)

        self.setObjectName("game-card")
        self.setFixedSize(160, 180)

        self._data = game

        # Main layout for the whole card
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(1, 1, 1, 1)
        self.main_layout.setSpacing(0)

        # Card Thumbnail
        self._card_thumbnail = QLabel()
        self._card_thumbnail.setText("NO GAME PHOTO")
        self._card_thumbnail.setAlignment(Qt.AlignCenter)
        self._card_thumbnail.setObjectName("card-thumbnail")
        self._card_thumbnail.setScaledContents(True)

        self.main_layout.addWidget(self._card_thumbnail)

        # Thumbnail layout ( Holds card's title )
        self.thumb_layout = QVBoxLayout(self._card_thumbnail)
        self.thumb_layout.setObjectName("card-thumb-layout")
        self.thumb_layout.setContentsMargins(0, 0, 0, 0)
        self.thumb_layout.setAlignment(Qt.AlignBottom)
        self._card_thumbnail.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Card Title
        self.card_label = QLabel(game.title)
        self.card_label.setObjectName("card-label")
        self.card_label.setWordWrap(True)
        self.card_label.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        self.card_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.thumb_layout.addWidget(self.card_label)


    @property
    def get_thumbnail(self):
        return self._card_thumbnail.pixmap()

    @get_thumbnail.setter
    def set_thumbnail(self, pixmap: QPixmap):
        scaled_pixmap = pixmap.scaled(pixmap.width(), pixmap.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

        rounded = QPixmap(scaled_pixmap.size())
        rounded.fill(Qt.transparent)

        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.Antialiasing)

        path = QPainterPath()
        path.addRoundedRect(0, 0, scaled_pixmap.width(), scaled_pixmap.height(), 12.0, 12.0)
        painter.setClipPath(path)

        painter.drawPixmap(0, 0, scaled_pixmap)
        painter.end()

        self._card_thumbnail.setPixmap(rounded)
        self._data.poster_pixmap = rounded
        self.thumb_loaded.emit(self._data.poster_pixmap)

    @property
    def get_data(self):
        if (self._data):
            return self._data

    @get_data.setter
    def set_data(self, game: GameData):
        self._data = game

    @property
    def get_id(self):
        if (self._id):
            return self._id
        return None


    def enterEvent(self, event):
        self.card_label.setAlignment(Qt.AlignCenter)
        self.thumb_layout.setAlignment(Qt.AlignCenter)

        self.style().unpolish(self)
        self.style().polish(self)

        super().enterEvent(event)

    def leaveEvent(self, event):
        self.card_label.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        self.thumb_layout.setAlignment(Qt.AlignBottom)

        self.style().unpolish(self)
        self.style().polish(self)

        super().leaveEvent(event)


    def mousePressEvent(self, event):
        if (event.button() is Qt.MouseButton.LeftButton):
            self.request_card.emit(self)
            super().mousePressEvent(event)
