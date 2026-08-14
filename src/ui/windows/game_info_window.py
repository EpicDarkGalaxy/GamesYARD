from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QLabel, QWidget, QFileDialog, QProgressBar, QHBoxLayout, QStyleFactory

from ...core.tools import get_logger
from ...core import MANAGER
from ...ui import Ui_gameinfo
from ...ui.widget.label import ClickableLabel

logger = get_logger(__name__)

class GameInfoWindow(QWidget):
    def __init__(self, game_card):
        super().__init__()

        self.setWindowTitle(f"Game Info - {game_card.title} ")
        self.setGeometry(100, 100, 600, 600)

        self.game_card = game_card
        self.links: list[ClickableLabel] = []

        self.ui = Ui_gameinfo()
        self.ui.setupUi(self)
        self.ui.fetch_btn.clicked.connect(self.on_fetch)
        self.ui.game_name_label.setText(game_card.title)

        self.set_poster(game_card.poster_pixmap)
        self.set_details(game_card.details.system_requirements)

    def set_poster(self, pixmap):
        self.ui.game_poster.setPixmap(pixmap)

    def set_details(self, details):
        logger.info("setting details")

        for catg, req in details.items():
            label = QLabel()
            label.setText(f"<b>{catg}</b>: {req}")
            self.ui.game_details_layout.addWidget(label)

    @Slot()
    def on_fetch(self):
        if (not self.game_card.details):
            return

        self.links.clear()

        download_links = MANAGER.get_download_links(self.game_card.url)
        for link in download_links:
            label = ClickableLabel()
            label.setProperty("styleClass","link-label")
            label.label.setText(f"<b>{link}</b>")
            label.raw_text = link
            label.label_text.connect(self.on_link_clicked)

            label.label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            label.label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

            self.links.append(label)
            self.ui.download_links_layout.addWidget(label)
            self.game_card.details.downloads_links.append(link)

    @Slot(float)
    def on_progress(self, progress):
        logger.info(f"downloading {progress}%")
        self.progress_bar.setValue(float(progress))

    # I will change it
    @Slot(str, object)
    def on_link_clicked(self, link, label: ClickableLabel):
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                text-align: center;
                color: white;
                background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 transparent, stop: 1 rgba(0, 0, 0, 220));
            }
        """)
        horizontal_layout = QHBoxLayout(label.label)
        horizontal_layout.setContentsMargins(0, 0, 0, 0)
        horizontal_layout.addWidget(self.progress_bar)
        print(link)
        file_path = QFileDialog.getSaveFileName(self, "Save File", "game.exe")
        if (file_path):
            MANAGER.download_game(file_path[0], link, self.on_progress)
