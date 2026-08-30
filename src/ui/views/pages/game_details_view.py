from PySide6.QtCore import Qt, Signal, Slot, QTimer
from PySide6.QtGui import QPixmap

from PySide6.QtWidgets import QWidget, QLabel, QGridLayout
from  typing import TYPE_CHECKING
from ...generated import Ui_GamePage
from ....core.utils import get_logger, get_icon_from_url, get_asset


if TYPE_CHECKING:
    from ...components import GameCard
    from ...view_models import GameDetailsViewModel

logger = get_logger(__name__)

class GameDetailsView(QWidget):
    def __init__(self, view_model: "GameDetailsViewModel"):
        super().__init__()
        self.ui = Ui_GamePage()
        self.ui.setupUi(self)
        self.view_model = view_model
        self.sys_req_widget = []
        self.gallery_widget = []

        self.bind_signals()

    def bind_signals(self):
        self.ui.btn_back.clicked.connect(lambda: self.view_model.nav.go_to("search"))
        self.ui.btn_back.clicked.connect(self._hide_all_widgets)

        # ViewModel
        self.view_model.set_title.connect(self.set_title)
        self.view_model.set_rating.connect(self.set_rating)
        self.view_model.set_release.connect(self.set_release)
        self.view_model.set_genres.connect(self.set_genres)
        self.view_model.set_poster.connect(self.set_poster)
        self.view_model.update_gallery.connect(self.populate_gallery)
        self.view_model.update_sys_req.connect(self.populate_requirements)

    def _ensure_widget(self, name: str, parent_layout, row: int, col: int) -> QLabel:
        """Creates a QLabel if it doesn't exist on the UI, adds it to the layout, and returns it."""
        if not hasattr(self.ui, name):
            new_widget = QLabel()
            setattr(self.ui, name, new_widget)
            parent_layout.addWidget(new_widget, row, col)
        return getattr(self.ui, name)

    def set_poster(self, poster_pixmap: QPixmap):
        logger.debug(f"Setting game poster. Input size: [{poster_pixmap.size().width()}]x[{poster_pixmap.size().height()}]")
        self.ui.game_poster.setFixedSize(320, 180)
        scaled_pixmap = poster_pixmap.scaled(
            320, 180,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        # Create a final pixmap to center-crop if the image doesn't match 16:9 exactly
        final_pixmap = scaled_pixmap.copy(
            (scaled_pixmap.width() - 320) // 2,
            (scaled_pixmap.height() - 180) // 2,
            320, 180
        )
        self.ui.game_poster.setScaledContents(False)
        self.ui.game_poster.setPixmap(final_pixmap)
        logger.debug("Game poster set and scaled successfully.")

    def set_title(self, title: str):
        logger.debug(f"Setting game title: [{title}]")
        widget = self._ensure_widget("game_title", self.ui.meta_info, 0, 0)
        widget.setText(str(title))
        widget.setStyleSheet("font-size: 18px; font-weight: bold;")

    def set_rating(self, rating: float | None, color: str):
        logger.debug(f"Setting game rating: [{rating}]")
        widget = self._ensure_widget("game_rating", self.ui.meta_info, 1, 0)
        if rating is not None:
            widget.setText(f"★ {rating:.1f}/5")
            widget.setStyleSheet(f"color: {color}; font-weight: bold;")
        else:
            widget.setText("N/A")
            widget.setStyleSheet("color: #aaaaaa;")

    def set_genres(self, genres: list[str]):
        logger.debug(f"Setting game genres: [{genres}]")
        widget = self._ensure_widget("game_genres", self.ui.meta_info, 2, 0)
        genre_text = ", ".join(genres) if genres else "N/A"
        widget.setText(f"Genres: {genre_text}")
        widget.setStyleSheet("color: #4da6ff; font-style: italic;")

    def set_release(self, year: int | str | None):
        logger.debug(f"Setting game release year: [{year}]")
        widget = self._ensure_widget("game_release_date", self.ui.meta_info, 3, 0)
        widget.setText(f"📅 Release Date: {year!s}")
        widget.setStyleSheet("color: #cccccc; font-size: 14px;")

    def set_metacritic(self, score: int | None, color: str):
        logger.debug(f"Setting game metacritic: [{score}]")
        widget = self._ensure_widget("game_metacritic", self.ui.meta_info, 4, 0)
        if score is not None:
            widget.setText(f'Metacritic: <span style="color: {color}; font-weight: bold;">{score}</span>')
            widget.setStyleSheet("color: #cccccc; font-size: 14px;")
        else:
            widget.setText("Metacritic: N/A")
            widget.setStyleSheet("color: #aaaaaa; font-size: 14px;")

    def _clear_layout(self, layout):
        if layout is None:
            return

        for i in reversed(range(layout.count())):
            item = layout.takeAt(i)
            widget = item.widget()

            if widget is not None:
                widget.hide()
                widget.deleteLater()

            if item.layout():
                item.layout().deleteLater()

    def populate_requirements(self, req_dict: dict, game_id: str = ""):
        # Hide all existing widgets instead of clearing/deleting to reuse them
        logger.debug(f"Hiding {len(self.sys_req_widget)} existing system requirement widgets.")
        for widget in self.sys_req_widget:
            widget.hide()

        logger.debug(f"Populating requirements for game: [{game_id}]")
        reqs = req_dict.get('requirements', {})

        if min_req := reqs.get("minimum"):
            logger.debug("Adding minimum requirements section.")
            self.add_section_to_grid("Minimum", min_req)

        if rec_req := reqs.get("recommended"):
            logger.debug("Adding recommended requirements section.")
            self.add_section_to_grid("Recommended", rec_req)

    def _get_pooled_label(self, text: str, style: str = "") -> QLabel:
        # Find a hidden widget or create a new one
        for widget in self.sys_req_widget:
            if not widget.isVisible():
                widget.setText(text)
                widget.setStyleSheet(style)
                widget.show()
                return widget

        # Create new if none available
        new_label = QLabel(text)
        new_label.setStyleSheet(style)
        self.sys_req_widget.append(new_label)
        return new_label

    def add_section_to_grid(self, section_name: str, specs: dict):
        row = self.ui.requirements_grid.rowCount()
        logger.debug(f"Adding section '[{section_name}]' to requirements grid at row [{row}].")

        # Add Section Header
        header = self._get_pooled_label(section_name, "font-weight: bold; color: #1e90ff; padding-top: 10px;")
        self.ui.requirements_grid.addWidget(header, row, 0, 1, 2)
        row += 1

        # Add Spec Rows
        for tag, value in specs.items():
            if value:
                lbl_tag = self._get_pooled_label(tag + ":", "color: #aaaaaa;")
                lbl_val = self._get_pooled_label(value)
                lbl_val.setWordWrap(True)

                self.ui.requirements_grid.addWidget(lbl_tag, row, 0)
                self.ui.requirements_grid.addWidget(lbl_val, row, 1)
                row += 1

    def populate_gallery(self, screenshots: list[bytes]):
        # Hide all existing gallery widgets to reuse them (pooling)
        for widget in self.gallery_widget:
            widget.hide()

        for shot in screenshots:
            QTimer.singleShot(0, lambda s=shot: self._add_pixmap_to_gallery(s))

    def _add_pixmap_to_gallery(self, shot_bytes: bytes):
        pixmap = QPixmap()
        pixmap.loadFromData(shot_bytes)

        # Find an existing hidden label or create a new one
        label = None
        for widget in self.gallery_widget:
            if not widget.isVisible():
                label = widget
                break

        if label is None:
            label = QLabel()
            self.gallery_widget.append(label)
            self.ui.gallery_layout.addWidget(label)

        label.setPixmap(pixmap.scaled(800, 200, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation))
        label.show()

    def _hide_all_widgets(self):
        """Hides all system requirement and gallery widgets."""
        for widget in self.sys_req_widget:
            widget.hide()
        for widget in self.gallery_widget:
            widget.hide()

    @Slot()
    def show_providers(self):
        pass
