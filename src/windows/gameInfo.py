from linecache import getline

from PySide6.QtCore import Slot
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QWidget

from ..core.fetcher import GameFetcher as gf
from ..core.log import get_logger
from ..core.models import GameCard
from ..ui.gameinfo_ui import Ui_gameinfo

logger = get_logger(__name__)

class GameInfoWindow(QWidget):
    def __init__(self, game_card: GameCard):
        super().__init__()

        self.setWindowTitle(f"Game Info - {game_card.title} ")
        self.setGeometry(100, 100, 600, 600)


        self.game_card = game_card
        self.links: list[QLabel]= []

        self.ui = Ui_gameinfo()
        self.ui.setupUi(self)
        self.ui.fetch_btn.clicked.connect(self.on_link_feth)

        self.set_poster(game_card.poster_pixmap)

        if (game_card.game_details):
            self.set_details(game_card.game_details.system_requirements)

    def set_poster(self, pixmap):
        self.ui.game_poster.setPixmap(pixmap)

    def set_details(self, details):
        logger.info("setting details")
        for catg, req in details.items():
            label = QLabel()
            label.setText(f"<b>{catg}</b>: {req}")
            self.ui.game_details_layout.addWidget(label)

    @Slot()
    def on_link_feth(self):
        if (not self.game_card.game_details):
            return

        self.links.clear()
        download_links = gf.fetch_download_links(self.game_card.game_url)
        for link in download_links:
            label = QLabel()
            label.setText(f"<b>{link}</b>")
            self.links.append(label)
            self.ui.download_links_layout.addWidget(label)
            self.game_card.game_details.downloads_links.append(link)
