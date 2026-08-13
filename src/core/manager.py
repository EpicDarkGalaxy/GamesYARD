from PySide6.QtCore import Slot
from PySide6.QtGui import QPixmap

from src.core.models.model_game_card import GameDetails

from ..core.asynchronus import (
    FetchWorkerSignals,
    GameFetchWorker,
    ThumbnailFetchWorker,
    ThumbnailWorkerSignals,
    WorkerManager,
    WorkerPool,
)
from ..core.models import GameCard
from ..ui.widget import GameCardWidget
from .tools import GameFetcher, get_default_icon, get_logger

logger = get_logger(__name__)

class AppState:
    def __init__(self):
        self.search_query = ""
        self.clear = False
        self.game_list: list[GameCard] = []

class _Manager:
    def __init__(self):
        self.app_state = AppState()
        self.game_fetcher = GameFetcher()
        self.worker_manager = WorkerManager()
        self.worker_pool = WorkerPool()
        self.main_window = None

    @Slot()
    def on_load_more(self):
        logger.info("Loading More")
        self.app_state.clear = False
        self.on_search(load_more=True)

    @Slot(GameCardWidget)
    def on_card_clicked(self, card_widget):
        logger.info(f"Card clicked: {card_widget.card.title}")
        card = card_widget.get_card()

        if (card):
            card_widget.card.details = GameDetails(self.get_system_req(card.url), [])
            self.main_window.show_game_info(card)

    @Slot(str)
    def on_search_text_changed(self, query: str):
        logger.info(f"Search text changed: {query}")
        self.app_state.search_query = query

    @Slot(bool)
    def on_search(self, load_more:bool=False):
        logger.info("on_search pressed!")

        self.main_window.update_fetch_btn("Fetching...", False)

        if (not load_more):
            self.app_state.clear = True

        # 2. Setup new signals
        self.game_fetch_signals = FetchWorkerSignals()
        self.game_fetch_signals.fetch_finished.connect(self.handle_search_result)

        # 3. Start new thread
        self.fetch_thread, self.fetch_worker = self.worker_manager.run_in_thread(
            GameFetchWorker(self.app_state.search_query, self.game_fetcher, self.game_fetch_signals, load_more)
        )

    @Slot(list)
    def handle_search_result(self, game_cards):
        logger.info("handle_search_result called")

        self.main_window.update_fetch_btn("Fetched", True)
        self.widgets: list[GameCardWidget] =[]

        self.thumb_fetched_signal = ThumbnailWorkerSignals()
        self.thumb_fetched_signal.thumbnail_fetch_finished.connect(self.on_thumbnail_fetched)

        for card in game_cards:
            card_widget = GameCardWidget(card, on_click=self.on_card_clicked)
            self.widgets.append(card_widget)

            self.thumb_fetch_thread = ThumbnailFetchWorker(card_widget, card.poster_url, self.thumb_fetched_signal)
            self.worker_pool.run_in_thread_pool(self.thumb_fetch_thread)

            self.app_state.game_list.append(card)
        self.main_window.append_to_grid(self.widgets)

    @Slot(GameCardWidget, bytes)
    def on_thumbnail_fetched(self, card_widget: GameCardWidget, img_data: bytes):
        card = card_widget.get_card()
        if (not card):
            return

        if img_data:
            logger.info(f"card {card.title} has thumbnail")
            pixmap = QPixmap()
            pixmap.loadFromData(img_data)

            if (not pixmap.isNull()):
                self.main_window.set_thumbnail(pixmap, card_widget)
            else:
                logger.info(f"card {card.title}, invalid pixmap, setting default")
                self.main_window.set_thumbnail(get_default_icon(), card_widget)
        else:
            logger.info(f"card {card_widget._card.title} does not have thumbnail, setting default")
            self.main_window.set_thumbnail(get_default_icon(), card_widget)

    def store_main_window(self, window):
        if (not self.main_window): # We don't want to store imposters
            logger.info(f"Storing main window: {window}")
            self.main_window = window

    def get_system_req(self, url: str):
        return self.game_fetcher.get_game_details(url)

    def get_download_links(self, url: str):
        return self.game_fetcher.fetch_download_links(url)

manager = _Manager()
