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

from src.core.asynchronus import worker_pool
from src.core.asynchronus.worker import game_fetch_worker, run_in_thread
from src.core.asynchronus.worker_pool import (
    ThumbnailFetchWorker,
    WorkerPool,
)
from src.core.fetcher import GameFetcher
from src.core.log import get_logger
from src.core.models import GameCardData
from src.core.signals import FetchWorkerSignals, ThumbnailWorkerSignals
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

        self.worker_pool = WorkerPool()

        self.gf = GameFetcher()
        self.search_query = ""
        self.cards_list = [] # GameCardData
        self.item_list: list[QListWidgetItem] = [] # QListWidgetItem

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
                                                        self.gf,
                                                        FetchWorkerSignals()
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

        self.thumb_signals = ThumbnailWorkerSignals()
        self.thumb_signals.thumbnail_fetch_finished.connect(self.on_thumbnail_fetched)

        for card in cards:
            item = QListWidgetItem()
            item.setText(card.title)
            self.item_list.append(item)
            listLayout.addItem(item)

            self.thumbnail_worker = ThumbnailFetchWorker(card, self.thumb_signals)
            self.worker_pool.run_in_thread_pool(self.thumbnail_worker)

    @Slot()
    def on_thumbnail_fetched(self, data_card, img_data):
        logger.debug(f"is data card null? {data_card is None} and is img data null? {img_data is None}")
        if (data_card):
            for card in self.item_list:
                if (data_card.title == card.text):
                    logger.info(f"is title same? {data_card.title == card.text}")
                    if (img_data):
                        pixmap = QPixmap()
                        pixmap.loadFromData(img_data)
                        self.set_thumbnail(QIcon(pixmap), card)
                    else:
                        self.set_thumbnail(QIcon(get_default_icon()), card)

    @Slot()
    def set_thumbnail(self, thumbnail: QIcon, item: QListWidgetItem):
        item.setIcon(thumbnail)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
