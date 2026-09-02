from typing import TYPE_CHECKING

from PySide6.QtCore import Qt, QTimer, Slot
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFileDialog, QLabel, QWidget

from src.core.utils import (
	get_filename_from_url,
	get_logger,
)
from src.ui.components import ProviderButton
from src.ui.generated import Ui_GamePage

if TYPE_CHECKING:
	from src.ui.view_models import GameDetailsViewModel

logger = get_logger(__name__)

class GameDetailsView(QWidget):
	def __init__(self, view_model: "GameDetailsViewModel"):
		super().__init__()
		self.ui = Ui_GamePage()
		self.ui.setupUi(self)
		self.ui.download_container.hide()

		self.view_model = view_model

		self.sys_req_widget: list[QLabel] = []
		self.gallery_widget: list[QLabel] = []

	def initialize(self):
		self.bind_signals()

	def bind_signals(self):
		self.ui.btn_back.clicked.connect(lambda: self.view_model.coordinator.navigate_back())
		self.ui.btn_get.clicked.connect(self.button_get)
		self.ui.btn_back.clicked.connect(self._hide_all_widgets)

		# ViewModel
		self.view_model.set_title.connect(self.set_title)
		self.view_model.set_rating.connect(self.set_rating)
		self.view_model.set_release.connect(self.set_release)
		self.view_model.set_genres.connect(self.set_genres)
		self.view_model.set_poster.connect(self.set_poster)
		self.view_model.update_gallery.connect(self.populate_gallery)
		self.view_model.update_sys_req.connect(self.populate_requirements)

		self.view_model.show_providers.connect(self.show_providers)
		self.view_model.get_providers_failed.connect(self.set_get_state)
		self.view_model.reset.connect(self.reset)

	# Buttons
	@Slot()
	def button_get(self):
		self.set_get_state("...", enabled=False)
		self.view_model.get_providers()

	def reset(self):
		self.ui.btn_get.show()
		self.ui.download_container.hide()
		self._clear_layout(self.ui.download_layout)
		self.set_get_state("Get", enabled=True)
		self._hide_all_widgets()

	@Slot(str, bool)
	def set_get_state(self, status: str, enabled=True):
		self.ui.btn_get.setText(status)
		self.ui.btn_get.setEnabled(enabled)

	@Slot(dict)
	def show_providers(self, providers: dict):
		self.ui.btn_get.hide()
		self._clear_layout(self.ui.download_layout)

		for provider_name, provider_url in providers.items():
			btn = ProviderButton(provider_name, provider_url)
			self.ui.download_layout.addWidget(btn)
		self.ui.download_container.show()

	def prompt_for_save_path(self, url: str) -> str:
		suggested_name = get_filename_from_url(url)
		file_path = QFileDialog.getSaveFileName(self, "Save Game", suggested_name)
		if (file_path[0] != ""):
			return file_path[0]
		return ""

	# Setters
	def set_poster(self, poster_data: bytes):
		if not poster_data:
			logger.warning("No poster data provided to set_poster.")
			return

		poster_pixmap = QPixmap()
		poster_pixmap.loadFromData(poster_data)
		self.ui.game_poster.setFixedSize(320, 180)
		scaled_pixmap = poster_pixmap.scaled(
			320, 180,
			Qt.AspectRatioMode.KeepAspectRatioByExpanding,
			Qt.TransformationMode.SmoothTransformation
		)
		final_pixmap = scaled_pixmap.copy(
			(scaled_pixmap.width() - 320) // 2,
			(scaled_pixmap.height() - 180) // 2,
			320, 180
		)
		self.ui.game_poster.setScaledContents(False)
		self.ui.game_poster.setPixmap(final_pixmap)

	def set_title(self, title: str):
		widget = self._ensure_widget("game_title", self.ui.meta_info, 0, 0)
		widget.setText(str(title))
		widget.setStyleSheet("font-size: 18px; font-weight: bold;")

	def set_rating(self, rating: float | None, color: str):
		widget = self._ensure_widget("game_rating", self.ui.meta_info, 1, 0)
		if rating is not None:
			widget.setText(f"★ {rating:.1f}/5")
			widget.setStyleSheet(f"color: {color}; font-weight: bold;")
		else:
			widget.setText("N/A")
			widget.setStyleSheet("color: #aaaaaa;")

	def set_genres(self, genres: list[str]):
		widget = self._ensure_widget("game_genres", self.ui.meta_info, 2, 0)
		genre_text = ", ".join(genres) if genres else "N/A"
		widget.setText(f"Genres: {genre_text}")
		widget.setStyleSheet("color: #4da6ff; font-style: italic;")

	def set_release(self, year: int | str | None):
		widget = self._ensure_widget("game_release_date", self.ui.meta_info, 3, 0)
		widget.setText(f"📅 Release Date: {year!s}")
		widget.setStyleSheet("color: #cccccc; font-size: 14px;")

	def set_metacritic(self, score: int | None, color: str):
		widget = self._ensure_widget("game_metacritic", self.ui.meta_info, 4, 0)
		if score is not None:
			widget.setText(f'Metacritic: <span style="color: {color}; font-weight: bold;">{score}</span>')
			widget.setStyleSheet("color: #cccccc; font-size: 14px;")
		else:
			widget.setText("Metacritic: N/A")
			widget.setStyleSheet("color: #aaaaaa; font-size: 14px;")

	# System Requirements & Gallery
	def populate_requirements(self, req_dict: dict, game_id: str = ""):
		for widget in self.sys_req_widget:
			widget.hide()

		reqs = req_dict.get('requirements', {})
		if min_req := reqs.get("minimum"):
			self.add_section_to_grid("Minimum", min_req)
		if rec_req := reqs.get("recommended"):
			self.add_section_to_grid("Recommended", rec_req)

	def add_section_to_grid(self, section_name: str, specs: dict):
		row = self.ui.requirements_grid.rowCount()
		header = self._get_pooled_label(section_name, "font-weight: bold; color: #1e90ff; padding-top: 10px;")
		self.ui.requirements_grid.addWidget(header, row, 0, 1, 2)
		row += 1

		for tag, value in specs.items():
			if value:
				lbl_tag = self._get_pooled_label(tag + ":", "color: #aaaaaa;")
				lbl_val = self._get_pooled_label(value)
				lbl_val.setWordWrap(True)
				self.ui.requirements_grid.addWidget(lbl_tag, row, 0)
				self.ui.requirements_grid.addWidget(lbl_val, row, 1)
				row += 1

	def populate_gallery(self, screenshots: list[bytes]):
		for widget in self.gallery_widget:
			widget.hide()
		for shot in screenshots:
			QTimer.singleShot(0, lambda s=shot: self._add_pixmap_to_gallery(s))

	def _add_pixmap_to_gallery(self, shot_bytes: bytes):
		pixmap = QPixmap()
		pixmap.loadFromData(shot_bytes)
		label = next((w for w in self.gallery_widget if not w.isVisible()), None)
		if label is None:
			label = QLabel()
			self.gallery_widget.append(label)
			self.ui.gallery_layout.addWidget(label)

		label.setPixmap(pixmap.scaled(800, 200, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation))
		label.show()

	# Helpers
	def _ensure_widget(self, name: str, parent_layout, row: int, col: int) -> QLabel:
		if not hasattr(self.ui, name):
			new_widget = QLabel()
			setattr(self.ui, name, new_widget)
			parent_layout.addWidget(new_widget, row, col)
		return getattr(self.ui, name)

	def _get_pooled_label(self, text: str, style: str = "") -> QLabel:
		for widget in self.sys_req_widget:
			if not widget.isVisible():
				widget.setText(text)
				widget.setStyleSheet(style)
				widget.show()
				return widget
		new_label = QLabel(text)
		new_label.setStyleSheet(style)
		self.sys_req_widget.append(new_label)
		return new_label

	def _clear_layout(self, layout):
		if layout is None:
			return
		for i in reversed(range(layout.count())):
			item = layout.takeAt(i)
			if widget := item.widget():
				widget.hide()
				widget.deleteLater()
			if item.layout():
				item.layout().deleteLater()

	def _hide_all_widgets(self):
		for widget in self.sys_req_widget:
			widget.hide()
		for widget in self.gallery_widget:
			widget.hide()
