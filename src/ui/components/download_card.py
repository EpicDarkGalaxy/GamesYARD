from typing import Optional

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QColor, QFont, QPainter, QPen, QPixmap
from PySide6.QtWidgets import QFrame, QHBoxLayout, QPushButton, QSizePolicy
from PySide6.QtGui import QEnterEvent, QPaintEvent
from PySide6.QtCore import QEvent

from src.core.utils import format_speed, get_logger

logger = get_logger(__name__)

class DownloadCard(QFrame):
	cancel: Signal = Signal(str)
	pause: Signal = Signal(str)
	resume: Signal = Signal(str)

	def __init__(self, id: str, title: str, file_size: int, resume_supported: bool = False, thumbnail: QPixmap | None = None):
		super().__init__()
		self.setFixedSize(300, 180)
		self.setSizePolicy(
			QSizePolicy.Policy.Expanding,
			QSizePolicy.Policy.Fixed,
		)
		self.button_layout: QHBoxLayout = QHBoxLayout(self)
		self.button_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
		self.button_layout.addStretch()

		self.button_height: float = (self.height() / 100) * 20

		self.cancel_button: QPushButton = QPushButton("Cancel", self)
		self.cancel_button.setFixedHeight(int(self.button_height))
		self.cancel_button.setStyleSheet("""
			QPushButton {
				background-color: #ff4d4d;
				border-radius: none;
			}
		""")
		self.cancel_button.hide()
		_ = self.cancel_button.clicked.connect(lambda: self.cancel.emit(self.id))


		self.pause_button: QPushButton = QPushButton("Pause", self)
		self.pause_button.setEnabled(resume_supported)
		self.pause_button.setFixedHeight(int(self.button_height))
		self.pause_button.setStyleSheet("border: none;")
		self.pause_button.hide()
		_ = self.pause_button.clicked.connect(self._handle_pause_button)

		self.button_layout.addWidget(self.pause_button)
		self.button_layout.addWidget(self.cancel_button)

		self.id: str = id
		self.title: str = title
		self.total_size: int = file_size
		self.thumbnail: Optional[QPixmap] = thumbnail
		self.downloaded_size: int = 0
		self.paused: bool = False
		self.progress: int = 0
		self.uniform_size: str = "40 / 900 MB"
		self.speed: str = ""

		self.anim_offset: float = 0.0

		self.anim_timer: QTimer = QTimer(self)
		self.anim_timer.setInterval(16)
		_ = self.anim_timer.timeout.connect(self._anim_tick)
		self.anim_timer.start()

		self.padding: int = 20
		self.is_hovered: bool = False

	def _anim_tick(self):
		self.anim_offset += 2.0
		if self.anim_offset > 300:
			self.anim_offset = 0.0
		self.update()

	def update_data(self, downloaded_size: int, total_size: int, progress: int, speed: float = 0.0, paused: bool = False, resume_supported: bool = False):
		self.downloaded_size = downloaded_size
		self.total_size = total_size
		self.progress = progress
		self.speed = format_speed(speed)
		self.paused = paused

		if self.total_size > 0:
			dl_mb = self.downloaded_size / (1024 * 1024)
			tot_mb = self.total_size / (1024 * 1024)
			self.uniform_size = f"{dl_mb:.1f} / {tot_mb:.1f} MB"
		else:
			dl_mb = self.downloaded_size / (1024 * 1024)
			self.uniform_size = f"{dl_mb:.1f} MB"

		self.update()

	def paintEvent(self, event: QPaintEvent):
		painter = QPainter(self)
		painter.setRenderHints(QPainter.RenderHint.Antialiasing)

		# 1. Background Thumbnail or Dark Grey
		if self.thumbnail:
			scaled = self.thumbnail.scaled(self.width(), self.height(), Qt.AspectRatioMode.KeepAspectRatioByExpanding)
			painter.drawPixmap(0, 0, scaled)
		else:
			painter.fillRect(0, 0, self.width(), self.height(), QColor(30, 30, 30))

		# 2. Dark Overlay for readability
		painter.fillRect(0, 0, self.width(), self.height(), QColor(20, 20, 20, 140))

		# 3. Progress Bar
		if self.progress > 0:
			progress_width = int(self.width() * self.progress / 100)
			painter.fillRect(0, 0, progress_width, self.height(), QColor(30, 144, 255, 70)) # Translucent Accent Blue

		# 4. Card Title (bottom-Left, Bold, Header-style)
		title_font = QFont("Segoe UI", 15, QFont.Weight.Bold)
		painter.setFont(title_font)
		painter.setPen(QColor(224, 224, 224))
		painter.drawText(15, self.height() - self.padding, self.title)

		# 5. Card Size (bottom-Right, DemiBold, Subtle)
		size_font = QFont("Segoe UI", 10, QFont.Weight.DemiBold)
		painter.setFont(size_font)
		painter.setPen(QColor(224, 224, 224))
		text = f"{self.uniform_size}"
		text_width = painter.fontMetrics().horizontalAdvance(text)
		painter.drawText(self.width() - text_width - 15, self.height() - self.padding, text)

		# 6. Card Speed (top-left, Normal, Subtle, outlined)
		speed_font = QFont("Segoe UI", 10, QFont.Weight.Normal)
		painter.setFont(speed_font)
		text = f"{self.speed}"

		# Draw outline
		painter.setPen(QPen(QColor(0, 0, 0), 2))
		for dx in (-1, 0, 1):
			for dy in (-1, 0, 1):
				if dx != 0 or dy != 0:
					painter.drawText(15 + dx, self.padding + 5 + dy, text)

		# Draw main text
		painter.setPen(QColor(30, 144, 255))  # Accent Blue
		painter.drawText(15, self.padding + 5, text)

		super().paintEvent(event)

	def _handle_pause_button(self):
		if not self.paused:
			self.pause_button.setText("Resume")
			self.pause.emit(self.id)
		else:
			self.pause_button.setText("Pause")
			self.resume.emit(self.id)

	def enterEvent(self, event: QEnterEvent):
		self.is_hovered = True
		self.pause_button.show()
		self.cancel_button.show()
		self.update()

	def leaveEvent(self, event: QEvent):
		self.is_hovered = False
		self.pause_button.hide()
		self.cancel_button.hide()
		self.update()
