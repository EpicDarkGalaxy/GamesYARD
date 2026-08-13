from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QLabel, QWidget

from ...core.tools import get_logger
from ...core import manager
from ...ui import Ui_gameinfo

logger = get_logger(__name__)

class GameInfoWindow(QWidget):
    def __init__(self, game_card):
        super().__init__()

        self.setWindowTitle(f"Game Info - {game_card.title} ")
        self.setGeometry(100, 100, 600, 600)

        self.game_card = game_card
        self.links: list[QLabel]= []

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

        download_links = manager.get_download_links(self.game_card.url)
        for link in download_links:
            label = QLabel()
            label.setProperty("styleClass","link-label")
            label.setText(f"<b>{link}</b>")

            label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

            self.links.append(label)
            self.ui.download_links_layout.addWidget(label)
            self.game_card.details.downloads_links.append(link)
