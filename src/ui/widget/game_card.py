from typing import override

from PySide6.QtCore import QRectF, Qt, Signal
from PySide6.QtGui import (
    QColor,
    QFont,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPixmap,
)
from PySide6.QtWidgets import QFrame

from ...core.tools.log import get_logger

logger = get_logger(__name__)

class GameCard(QFrame):
    clicked = Signal(object)

    def __init__(self, game_data):
        super().__init__()
        self.setFixedSize(320, 180)  # Native 16:9 banner size
        self.setObjectName("game-card")
        self.id = str(game_data.id)
        self.title = game_data.title
        self.rating = game_data.rating
        self.banner_url = game_data.background_image
        self.banner = QPixmap()

    @property
    def thumbnail(self):
        return self.banner

    @thumbnail.setter
    def thumbnail(self, img_data: bytes):
        if img_data:
            logger.info(f"Thumbnail stored for ID: [{self.title}]")
            self.banner.loadFromData(img_data)
            self.update()
        else:
            logger.warning(f"IMG data is null for ID [{self.title}]")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.RenderHint.Antialiasing |
            QPainter.RenderHint.SmoothPixmapTransform |
            QPainter.RenderHint.TextAntialiasing
        )

        rect = QRectF(0, 0, self.width(), self.height())

        # 1. Rounded Card Borders (10px radius)
        clip_path = QPainterPath()
        clip_path.addRoundedRect(rect, 10.0, 10.0)
        painter.setClipPath(clip_path)

        # 2. Draw Scaled Background Image
        if not self.banner.isNull():
            scaled = self.banner.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            x = (self.width() - scaled.width()) / 2.0
            y = (self.height() - scaled.height()) / 2.0
            painter.drawPixmap(int(x), int(y), scaled)
        else:
            painter.fillRect(rect, QColor("#1e1e24"))

        # 3. Draw Bottom Gradient Overlay for Text Readability
        gradient = QLinearGradient(0, self.height() * 0.35, 0, self.height())
        gradient.setColorAt(0.0, QColor(0, 0, 0, 0))        # Transparent
        gradient.setColorAt(0.6, QColor(0, 0, 0, 160))      # Semi-dark
        gradient.setColorAt(1.0, QColor(0, 0, 0, 230))      # Dark backdrop
        painter.fillRect(rect, gradient)

        # 4. Draw Game Title
        painter.setPen(QColor("#FFFFFF"))
        painter.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        title_rect = QRectF(14, self.height() - 52, self.width() - 28, 22)

        # Elide (truncate with "...") if title is too long
        metrics = painter.fontMetrics()
        elided_title = metrics.elidedText(self.title, Qt.TextElideMode.ElideRight, int(title_rect.width()))
        painter.drawText(title_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, elided_title)

        # 5. Draw Rating
        painter.setPen(QColor("#FBBF24"))  # Gold accent
        painter.setFont(QFont("Segoe UI", 9, QFont.Weight.DemiBold))
        rating_rect = QRectF(14, self.height() - 28, self.width() - 28, 18)
        painter.drawText(rating_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, f"★ {self.rating:.1f}")

    @override
    def mousePressEvent(self, event):
        if event.button() is Qt.MouseButton.LeftButton:
            self.clicked.emit(self)
            return super().mousePressEvent(event)
