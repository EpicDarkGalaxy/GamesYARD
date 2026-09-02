from typing import override

from PySide6.QtCore import (
	Property,
	QEasingCurve,
	QPropertyAnimation,
	QRectF,
	Qt,
	Signal,
	Slot
)
from PySide6.QtGui import (
	QColor,
	QFont,
	QLinearGradient,
	QPainter,
	QPainterPath,
	QPixmap,
)
from PySide6.QtWidgets import QFrame

from src.core.utils import get_logger
from src.core.aio.workers import Worker

logger = get_logger(__name__)

class GameCard(QFrame):
	request_thumbnail = Signal(str, str)
	thumb_loaded = Signal(QPixmap)
	clicked = Signal(object)

	def __init__(self, game_data, model):
		super().__init__()
		self.setFixedSize(320, 180)  # Native 16:9 banner size
		self.setObjectName("game-card")
		self.id: str = str(game_data.id)
		self.title: str = game_data.title
		self.rating: float = float(game_data.rating)
		self.banner_url: str = game_data.background_image
		self.sys_req: dict = game_data.system_requirements
		self.released: str = game_data.released
		self.genres: list = game_data.genres
		self.metacritic: int = game_data.metacritic
		self.banner: QPixmap = QPixmap()

		self.model = model
		self.worker_dispatched = False

		self._hover_opacity = 0.0
		self.setMouseTracking(True)

		self.anim = QPropertyAnimation(self, b"hover_opacity")
		self.anim.setDuration(200)
		self.anim.setEasingCurve(QEasingCurve.Type.InCubic)

	def _get_hover_opacity(self):
		return self._hover_opacity

	def _set_hover_opacity(self, value):
		self._hover_opacity = value
		self.update()

	hover_opacity = Property(float, _get_hover_opacity, _set_hover_opacity)

	@property
	def thumbnail(self):
		return self.banner

	@thumbnail.setter
	def thumbnail(self, img_data: bytes):
		if img_data and isinstance(img_data, bytes):
			logger.info(f"Thumbnail stored for ID: [{self.title}]")
			_ = self.banner.loadFromData(img_data)
			self.thumb_loaded.emit(self.banner)
			self.update()
		else:
			logger.warning(f"IMG data is null for ID [{self.title}]")

	@Slot(bytes, str)
	def _handle_thumb(self, img_data: bytes, card_id):
		if card_id == self.id:
			self.thumbnail = img_data


	def enterEvent(self, event):
		self.anim.setStartValue(self._hover_opacity)
		self.anim.setEndValue(1.0)
		self.anim.start()
		super().enterEvent(event)

	def leaveEvent(self, event):
		self.anim.setStartValue(self._hover_opacity)
		self.anim.setEndValue(0.0)
		self.anim.start()
		super().leaveEvent(event)

	def mousePressEvent(self, event):
		if event.button() is Qt.MouseButton.LeftButton:
			self.clicked.emit(self)
			return super().mousePressEvent(event)

	@override
	def showEvent(self, event) -> None:
		if self.isVisible() and self.banner.isNull() and not self.worker_dispatched:
			self.worker_dispatched = True
			worker = Worker(self.model.asset_manager.get_thumbnail, self.id, self.banner_url, context=self.id)
			_ = worker.signals.result_ready.connect(self._handle_thumb)
			self.model.task_runner.run(worker)
		return super().showEvent(event)
