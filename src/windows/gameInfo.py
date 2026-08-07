from PySide6.QtCore import Slot
from PySide6.QtWidgets import QLabel, QWidget

from ..core.fetcher import GameFetcher as gf
from ..core.models import GameDetails
from ..ui.gameinfo_ui import Ui_gameinfo


class GameInfoWindow(QWidget):
    def __init__(self, game_details: GameDetails):
        super().__init__()
        self.setWindowTitle(f"Game Info - {game_details.title} ")
        self.setGeometry(100, 100, 600, 600)

        self.game_details = game_details

        self.ui = Ui_gameinfo()
        self.ui.setupUi(self)

        self.ui.game_poster.setPixmap(game_details.posterPixmap)
        self.ui.game_name_label.setText(game_details.title)

        self.ui.fetch_btn.clicked.connect(self.on_fetch)

        for catg, req in game_details.system_requirements.items():
            label = QLabel()
            label.setText(f"<b>{catg}</b>: {req}")
            self.ui.game_details_layout.addWidget(label)

    @Slot()
    def on_fetch(self):
        download_links = gf.fetch_download_links(self.game_details.href)
        for link in download_links:
            label = QLabel()
            label.setText(f"<b>{link}</b>")
            self.ui.download_links_layout.addWidget(label)
            self.game_details.downloads_links.append(link)
