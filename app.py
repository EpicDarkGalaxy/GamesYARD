import os
import sys

from PySide6.QtCore import QSize, Qt, Slot
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
)

from src.core.asynchronus import (
    FetchWorkerSignals,
    GameFetchWorker,
    ThumbnailFetchWorker,
    ThumbnailWorkerSignals,
    WorkerManager,
    WorkerPool,
)
from src.core.models import GameCard, GameDetails
from src.core.tools import GameFetcher, get_default_icon, get_logger
from src.ui import Ui_MainWindow
from src.windows import GameInfoWindow

logger = get_logger(__name__)

def load_stylesheet(app: QApplication):
    # Construct path to style.qss
    style_path = os.path.join(os.path.dirname(__file__), "src", "ui", "style.qss")

    if os.path.exists(style_path):
        with open(style_path, "r") as f:
            app.setStyleSheet(f.read())
    else:
        print(f"Warning: Stylesheet not found at {style_path}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("4fnet FrontEnd")
        self.resize(500, 400)

        self.main_ui = Ui_MainWindow()
        self.main_ui.setupUi(self)

        self.worker_pool = WorkerPool()
        self.worker_manager = WorkerManager

        # Section start
        # This section maybe get removed from here later, and done from PySide6-Designer
        list_widget = self.main_ui.game_cards_list_widget

        list_widget.setIconSize(QSize(150, 200))
        list_widget.setGridSize(QSize(170, 250))

        list_widget.setSpacing(10)
        list_widget.setWordWrap(True)
        # Section end

        self.game_fetcher = GameFetcher()
        self.search_query = ""

        # Cards list
        self.cards_list: dict[str, QListWidgetItem] = {}
        self.main_ui.game_cards_list_widget.clicked.connect(self.on_card_clicked)

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search only games")
        self.search_bar.setClearButtonEnabled(True)
        self.search_bar.returnPressed.connect(self.on_search)
        self.search_bar.textChanged.connect(self.on_search_text_changed)

        # Fetch button
        self.fetch_btn = QPushButton()
        self.fetch_btn.clicked.connect(self.on_search)
        self.fetch_btn.setText("Fetch")

        # Add to toolbar
        self.main_ui.toolBar.addWidget(self.search_bar)
        self.main_ui.toolBar.addWidget(self.fetch_btn)

    @Slot(str)
    def on_search_text_changed(self, text: str):
        self.search_query = text.strip()

    @Slot()
    def on_search(self,):
        logger.info("on_search pressed!")

        self.fetch_btn.setText("Fetching...")
        self.fetch_btn.setEnabled(False)

        # 2. Setup new signals
        self.game_fetch_signals = FetchWorkerSignals()
        self.game_fetch_signals.fetch_finished.connect(self.populate_grid)

        # 3. Start new thread
        self.fetch_thread, self.fetch_worker = self.worker_manager.run_in_thread(
            GameFetchWorker(self.search_query, self.game_fetcher, self.game_fetch_signals)
        )

    @Slot()
    def on_card_clicked(self, card: QListWidgetItem):
        card_data: GameCard = card.data(Qt.ItemDataRole.UserRole)
        card_data.game_details = GameDetails(self.game_fetcher.get_game_details(card_data.game_url), [])

        logger.info(f"on_card_clicked called with {card_data}")

        self.gameinfo = GameInfoWindow(card_data)
        self.gameinfo.show()

    @Slot(list)
    def populate_grid(self, games: list[GameCard]):
        logger.info(f"populate_grid called with {len(games)} cards")

        self.fetch_btn.setText("Fetched!")
        self.fetch_btn.setEnabled(True)
        self.cards_list.clear()

        listLayout = self.main_ui.game_cards_list_widget

        listLayout.clear()

        self.thumb_signals = ThumbnailWorkerSignals()
        self.thumb_signals.thumbnail_fetch_finished.connect(self.on_thumbnail_fetched)

        for game in games:
            logger.info(f"adding {game.title} to Grid")
            card = QListWidgetItem()
            card.setData(Qt.ItemDataRole.UserRole, game)
            card.setText(game.title)
            self.cards_list[game.title] = card
            listLayout.addItem(card)

            self.thumbnail_worker = ThumbnailFetchWorker(card, game.poster_link, self.thumb_signals)
            self.worker_pool.run_in_thread_pool(self.thumbnail_worker)

    @Slot(QListWidgetItem, bytes)
    def on_thumbnail_fetched(self, card: QListWidgetItem, img_data):
        logger.debug(f"is img data null? {img_data is None}")
        if img_data and card:
            logger.info(f"card {card.text()} has thumbnail, setting it")
            pixmap = QPixmap(150, 150)
            pixmap.loadFromData(img_data)
            self.set_thumbnail(QIcon(pixmap), card)
        else:
            logger.info(f"card {card.text()} does not have thumbnail, setting default")
            self.set_thumbnail(QIcon(get_default_icon()), card)

    @Slot()
    def set_thumbnail(self, thumbnail: QIcon, item: QListWidgetItem):
        logger.info(f"setting icon for {item.text()}")
        game_card = item.data(Qt.ItemDataRole.UserRole)
        if game_card:
            logger.info(f"storing thumbnail for {game_card.title} in its CardData")
            game_card.poster_pixmap = thumbnail.pixmap(150,150)
        item.setIcon(thumbnail)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    load_stylesheet(app)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
