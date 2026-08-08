import sys

from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QLineEdit,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
)

from src.core.asynchronus.worker import game_fetch_worker, run_in_thread
from src.core.asynchronus.worker_pool import (
    IconFetchWorker,
    run_in_thread_pool,
    worker_pool,
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
        self.cards_list = [] # GameCardData
        self.item_list = [] # QListWidgetItem

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
        self.fetch_thread, self.fetch_worker = run_in_thread(
                                                    game_fetch_worker(
                                                        self.search_query,
                                                        self.gf
                                                    ),
                                                    self.populate_grid
                                                )

    @Slot(list)
    def populate_grid(self, cards: list[GameCardData]):
        self.cards_list.clear()
        self.item_list.clear()

        listLayout = self.main_ui.game_cards_list_widget
        self.cards_list = cards

        listLayout.clear()

        for card in cards:
            item = QListWidgetItem()
            item.setText(card.title)
            self.item_list.append(item)
            listLayout.addItem(item)
            worker = IconFetchWorker(card.posterLink)
            run_in_thread_pool(worker, self.set_icons)

        # for card in cards:


    @Slot()
    def set_icons(self, img_data: bytes):
        pixmap = QPixmap()
        pixmap.loadFromData(img_data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
