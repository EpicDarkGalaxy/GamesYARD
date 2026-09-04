from PySide6.QtWidgets import QStyle, QStyleOptionViewItem, QStyledItemDelegate
from PySide6.QtGui import QPainter, QPainterPath, QColor, QFont, QLinearGradient
from PySide6.QtCore import QModelIndex, Qt, QRectF, QSize
from src.core.utils.log import get_logger

logger = get_logger(__name__)

class GameCardDelegate(QStyledItemDelegate):
	def paint(self, painter: QPainter, option, index):
		# The game object is stored in the model's data
		game = index.data(Qt.ItemDataRole.DisplayRole)
		if not game:
			return

		painter.save()
		painter.setRenderHints(
			QPainter.RenderHint.Antialiasing |
			QPainter.RenderHint.SmoothPixmapTransform |
			QPainter.RenderHint.TextAntialiasing
		)

		# 'option.rect' is the area provided by the QListView for this item
		rect = QRectF(option.rect).adjusted(10, 10, -10, -10)

		# 1. Rounded Card Borders
		clip_path = QPainterPath()
		clip_path.addRoundedRect(rect, 10.0, 10.0)
		painter.setClipPath(clip_path)

		# 2. Draw Background
		thumb_dict = index.model().thumbnails.get(index.row())
		thumb = thumb_dict.get(game.id) if thumb_dict else None

		if thumb and not thumb.isNull():
			# logger.debug(f"Drawing thumbnail for row: {index.row()}")
			painter.drawPixmap(rect.toRect(), thumb)
		else:
			painter.fillRect(rect, QColor("#1e1e24"))
			# Trigger the fetch if it's the first time
			logger.debug(f"Fetching thumbnail for game: {game.id}")
			index.model().fetch_thumbnail(index.row(), str(game.id), game.background_image)

		# 3. Draw Bottom Gradient Overlay for Text Readability
		gradient = QLinearGradient(0, rect.bottom() * 0.35, 0, rect.bottom())
		gradient.setColorAt(0.0, QColor(0, 0, 0, 0))        # Transparent
		gradient.setColorAt(0.6, QColor(0, 0, 0, 160))      # Semi-dark
		gradient.setColorAt(1.0, QColor(0, 0, 0, 230))      # Dark backdrop
		painter.fillRect(rect, gradient)

		# 4. Draw Title
		painter.setPen(QColor("#FFFFFF"))
		painter.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
		title_rect = QRectF(rect.x() + 14, rect.bottom() - 40, rect.width() - 28, 22)
		painter.drawText(title_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, game.title)

		# 5. Draw Rating
		painter.setPen(QColor("#FBBF24"))
		painter.setFont(QFont("Segoe UI", 9, QFont.Weight.DemiBold))
		rating_rect = QRectF(rect.x() + 14, rect.bottom() - 20, rect.width() - 28, 18)
		painter.drawText(rating_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, f"★ {game.rating:.1f}")

        # 6. Draw Hover Effect
		if index.isValid():
			if option.state & QStyle.State_MouseOver:
				hover_overlay = QLinearGradient(0, 0, rect.width(), rect.height()) # Cover Full CARD
				hover_overlay.setColorAt(0.0, QColor(0, 0, 0, 0)) # Transparent
				hover_overlay.setColorAt(1.0, QColor(0, 0, 0, 100))# Dark overlay
				hover_overlay.setColorAt(0.5, QColor(0, 0, 0, 50)) # Mid-dark

				painter.fillRect(rect, hover_overlay)

		painter.restore()

	def sizeHint(self, option, index):
		return QSize(320, 180)
