from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap

from PySide6.QtWidgets import QWidget, QLabel, QGridLayout
from ...game_page_ui import Ui_GamePage
from ....core.tools.log import get_logger

logger = get_logger(__name__)

class GamePageView(QWidget):
    back = Signal()

    def __init__(self):
        super().__init__()
        self.ui = Ui_GamePage()
        self.ui.setupUi(self)
        self.current_game_id = ""
        self.ui.btn_back.clicked.connect(lambda: self.back.emit())

    def display(self, game_card):
        if game_card:
            self.current_game_id = game_card.id
            logger.debug(f"Current viewing card id: {self.current_game_id}")
            if game_card.banner:
                self.ui.game_poster.setPixmap(game_card.banner)
            else:
                black_pixmap = QPixmap(self.ui.game_poster.size())
                black_pixmap.fill(Qt.black)
                self.set_poster(black_pixmap)
            self.ui.game_title.setText(game_card.title)

    def set_poster(self, poster_pixmap: QPixmap):
        self.ui.game_poster.setFixedSize(320, 180)
        scaled_pixmap = poster_pixmap.scaled(
            poster_pixmap.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )
        self.ui.game_poster.setPixmap(scaled_pixmap)

    def clear_layout(self, layout):
        if layout is None:
            return

        # 1. Loop backwards (safer when removing items)
        for i in reversed(range(layout.count())):
            item = layout.takeAt(i)
            widget = item.widget()

            if widget is not None:
                # 2. Hide before deleting to prevent flicker
                widget.hide()
                # 3. Schedule for deletion safely
                widget.deleteLater()

            # 4. If the item was a layout (like a nested one), delete it too
            if item.layout():
                item.layout().deleteLater()

    def reset_req_grid(self):
        # Just clear the contents, don't delete the grid object itself!
        if hasattr(self.ui, "requirements_grid") and self.ui.requirements_grid:
            self.clear_layout(self.ui.requirements_grid)

    def populate_requirements(self, req_dict, game_id: str):
        if game_id != self.current_game_id:
            logger.debug(f"Requested to display req for [{game_id}] but user is viewing [{self.current_game_id}], aborting...")
            return
        self.reset_req_grid()

        # 2. Add rows for Minimum
        self.add_section_to_grid("Minimum", req_dict['minimum'])

        # 3. Add rows for Recommended
        self.add_section_to_grid("Recommended", req_dict['recommended'])

    def add_section_to_grid(self, section_name, specs):
        row = self.ui.requirements_grid.rowCount()

        # Add Section Header
        header = QLabel(section_name)
        header.setStyleSheet("font-weight: bold; color: #1e90ff; padding-top: 10px;")
        self.ui.requirements_grid.addWidget(header, row, 0, 1, 2)
        row += 1

        # Add Spec Rows
        for tag, value in specs.items():
            if value: # Only show if there is data
                lbl_tag = QLabel(tag + ":")
                lbl_tag.setStyleSheet("color: #aaaaaa;")

                lbl_val = QLabel(value)
                lbl_val.setWordWrap(True)

                self.ui.requirements_grid.addWidget(lbl_tag, row, 0)
                self.ui.requirements_grid.addWidget(lbl_val, row, 1)
                row += 1
