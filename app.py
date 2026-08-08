import sys

from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QLineEdit,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
)

from src.core.fetcher import GameFetcher
from src.core.log import get_logger
from src.core.models import GameCardData
from src.core.utils import get_default_icon
from src.ui.main_window_ui import Ui_MainWindow
from src.windows.gameInfo import GameInfoWindow

logger = get_logger(__name__)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("4fnet FrontEnd")
        self.resize(500, 400)

        self.main_ui = Ui_MainWindow()
        self.main_ui.setupUi(self)

        self.gf = GameFetcher()
        self.search_query = ""
        self.cards_list = []

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search")
        self.search_bar.setClearButtonEnabled(True)
        self.search_bar.returnPressed.connect(self.on_search_pressed)

        # Fetch button
        self.fetch_btn = QPushButton()
        self.fetch_btn.clicked.connect(self.on_search_pressed)
        self.fetch_btn.setText("Fetch")

        # Add to toolbar
        self.main_ui.toolBar.addWidget(self.search_bar)
        self.main_ui.toolBar.addWidget(self.fetch_btn)

    @Slot()
    def on_search_pressed(self):
        logger.info("on_search pressed!")

    @Slot(list)
    def populate_grid(self, cards: list[GameCardData]):
        listLayout = self.main_ui.game_cards_list_widget

        # clearing before adding
        listLayout.clear()

        placeholder_icon = QIcon(get_default_icon())
        for card in cards:
            item = QListWidgetItem()
            item.setText(card.title)
            item.setIcon(placeholder_icon)
            listLayout.addItem(item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
