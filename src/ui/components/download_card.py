from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont, QLinearGradient, QPainter, QPen
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QSizePolicy

from src.core.utils import get_logger, format_speed

logger = get_logger(__name__)

class DownloadCard(QFrame):
    def __init__(self, id: str, title: str, file_size: int):
        super().__init__()
        self.setFixedHeight(30)  # Slightly taller to comfortably fit text
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        self.id = id
        self.title = title
        self.total_size = file_size
        self.downloaded_size = 0
        self.progress = 0

        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 0, 15, 0)

        # Title Label matching app font color (#e0e0e0)
        self.title_label = QLabel(self.title, self)
        font = QFont("Segoe UI", 10, QFont.Weight.Bold)
        self.title_label.setFont(font)
        self.title_label.setStyleSheet("color: #e0e0e0; background: transparent;")
        layout.addWidget(self.title_label)

        layout.addStretch()

        # Speed Label matching muted text style (#888888)
        self.speed_label = QLabel("0 MB/s")
        speed_font = QFont("Segoe UI", 9)
        self.speed_label.setFont(speed_font)
        self.speed_label.setStyleSheet("color: #888888; background: transparent;")
        layout.addWidget(self.speed_label)

        layout.addSpacing(10)

        # File Size Label matching muted text style (#888888)
        self.size_label = QLabel("0/0 MB")
        size_font = QFont("Segoe UI", 9)
        self.size_label.setFont(size_font)
        self.size_label.setStyleSheet("color: #888888; background: transparent;")
        layout.addWidget(self.size_label)

        layout.addSpacing(10)

        # Percentage / Status Label matching accent blue (#1e90ff)
        self.status_label = QLabel("0%", self)
        status_font = QFont("Segoe UI", 10, QFont.Weight.Bold)
        self.status_label.setFont(status_font)
        self.status_label.setStyleSheet("color: #1e90ff; background: transparent;")
        layout.addWidget(self.status_label)

    def update_data(self, downloaded_size: int, total_size: int, progress: int, speed: float = 0.0):
        self.downloaded_size = downloaded_size
        self.total_size = total_size
        self.progress = progress

        # Update status and size text
        self.status_label.setText(f"{self.progress}%")
        self.speed_label.setText(format_speed(speed))

        # Convert bytes/sizes nicely if needed, assuming bytes or MB based on original init
        # For simplicity, format downloaded/total if total is available
        if self.total_size > 0:
            dl_mb = self.downloaded_size / (1024 * 1024)
            tot_mb = self.total_size / (1024 * 1024)
            self.size_label.setText(f"{dl_mb:.1f} / {tot_mb:.1f} MB")
        else:
            dl_mb = self.downloaded_size / (1024 * 1024)
            self.size_label.setText(f"{dl_mb:.1f} MB")
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)

        # Background matching app's card style (#1e1e1e with subtle gradient)
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(30, 30, 30))  # #1e1e1e
        gradient.setColorAt(1, QColor(22, 22, 22))
        painter.setBrush(gradient)

        # Border matching app border style (#333333)
        pen = QPen(QColor(51, 51, 51), 1)
        painter.setPen(pen)
        painter.drawRoundedRect(0, 0, self.width() - 1, self.height() - 1, 8, 8)

        # Progress overlay matching the app's accent gradient (#1e90ff)
        progress_width = int((self.width() - 2) * self.progress / 100)
        if progress_width > 0:
            progress_gradient = QLinearGradient(0, 0, progress_width, 0)
            # Uses your app's primary blue theme with smooth transparency
            progress_gradient.setColorAt(0, QColor(30, 144, 255, 60))  # #1e90ff faded
            progress_gradient.setColorAt(
                1, QColor(30, 144, 255, 100)
            )  # #1e90ff slightly bolder

            painter.setBrush(progress_gradient)
            painter.setPen(Qt.PenStyle.NoPen)
            # Draw inside the border (1px offset)
            painter.drawRoundedRect(1, 1, progress_width, self.height() - 2, 7, 7)

        # Let Qt handle child layouts (labels)
        super().paintEvent(event)

    def enterEvent(self, event):
        return super().enterEvent(event)
