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

from src.core.asynchronus.worker import GameFetchWorker, WorkerManager
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
        self.worker_manager = WorkerManager

        self.gf = GameFetcher()
        self.search_query = ""
        self.cards_list = []  # GameCardData
        self.items_list: dict[str, QListWidgetItem] = {}  # QListWidgetItem

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search")
        self.search_bar.setClearButtonEnabled(True)
        self.search_bar.returnPressed.connect(self.on_search_pressed)
        self.search_bar.textChanged.connect(self.on_search_text_changed)

        # Fetch button
        self.fetch_btn = QPushButton()
        self.fetch_btn.clicked.connect(self.on_search_pressed)
        self.fetch_btn.setText("Fetch")

        # Add to toolbar
        self.main_ui.toolBar.addWidget(self.search_bar)
        self.main_ui.toolBar.addWidget(self.fetch_btn)

    @Slot(str)
    def on_search_text_changed(self, text: str):
        self.search_query = text.strip()

    @Slot()
    def on_search_pressed(self):
        logger.info("on_search pressed!")
        self.fetch_btn.setEnabled(False)

        # 2. Setup new signals
        self.game_fetch_signals = FetchWorkerSignals()
        self.game_fetch_signals.fetch_finished.connect(self.populate_grid)

        # 3. Start new thread
        self.fetch_thread, self.fetch_worker = self.worker_manager.run_in_thread(
            GameFetchWorker(self.search_query, self.gf, self.game_fetch_signals)
        )

    @Slot(list)
    def populate_grid(self, cards: list[GameCardData]):
        self.fetch_btn.setEnabled(True)

        self.cards_list.clear()
        self.items_list.clear()
        self.cards_list = cards

        listLayout = self.main_ui.game_cards_list_widget

        listLayout.clear()

        self.thumb_signals = ThumbnailWorkerSignals()
        self.thumb_signals.thumbnail_fetch_finished.connect(self.on_thumbnail_fetched)

        for card in cards:
            logger.info(f"adding {card.title} to Grid")
            item = QListWidgetItem()
            item.setText(card.title)
            self.items_list[card.title] = item
            listLayout.addItem(item)

            self.thumbnail_worker = ThumbnailFetchWorker(card, self.thumb_signals)
            self.worker_pool.run_in_thread_pool(self.thumbnail_worker)

    @Slot()
    def on_thumbnail_fetched(self, data_card, img_data):
        logger.debug(
            f"is data card null? {data_card is None} and is img data null? {img_data is None}"
        )

        for title, item in self.items_list.items():
            if img_data:
                logger.info(
                    f"\nGAME title ({data_card.title})"
                    f"\nComparing with"
                    f"\nITEM title ({title})"
                    f"\nIS title same? {data_card.title == title}"
                )
                if data_card.title == title:
                    pixmap = QPixmap(150, 150)
                    pixmap.loadFromData(img_data)
                    self.set_thumbnail(QIcon(pixmap), item)
            else:
                self.set_thumbnail(QIcon(get_default_icon()), item)

    @Slot()
    def set_thumbnail(self, thumbnail: QIcon, item: QListWidgetItem):
        logger.info(f"setting icon for {item.text()}")
        item.setIcon(thumbnail)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
