from enum import Enum

from PySide6.QtCore import Signal, Slot
from PySide6.QtGui import QPixmap

from src.core.asynchronus.worker import DownloadWorker
from src.core.downloaders import DownloaderFactory
from src.core.tools.utils import get_direct_link, get_filename_from_url, get_site_name

from ..core.asynchronus import (
    DownloadWorkerSignals,
    FetchWorkerSignals,
    GameFetchWorker,
    ThumbnailFetchWorker,
    ThumbnailWorkerSignals,
    WorkerManager,
    WorkerPool,
)
from ..core.models import GameData
from ..ui import ManagerSignals
from ..ui.widget import GameCard
from .tools import GameFetcher, get_default_icon, get_logger

logger = get_logger(__name__)

class FetchState(Enum):
    READY = 1
    FETCHING = 2
    FETCHED = 3
    FETCH_FAIL = 4

class AppState:
    def __init__(self, manager):
        self.manager = manager
        self.search_query = ""
        self._fetch_state = FetchState.READY
        self.clear_grid = False
        self.is_downloading = False
        self.providers = []
        self.download_queue = []
        self.game_list: list[GameData] = []

    @property
    def get_fetch_state(self) -> FetchState:
        return self._fetch_state

    @get_fetch_state.setter
    def set_fetch_state(self, state: FetchState):
        self._fetch_state = state
        if (self._fetch_state is FetchState.READY):
            self.manager.signals.update_fetch_btn.emit("Ready", True)
        elif (self._fetch_state is FetchState.FETCHING):
            self.manager.signals.update_fetch_btn.emit("Fetching", False)
        elif (self._fetch_state is FetchState.FETCHED):
            self.manager.signals.update_fetch_btn.emit("Fetched", True)
        elif (self._fetch_state is FetchState.FETCH_FAIL):
            self.manager.signals.update_fetch_btn.emit("Fetch Fail", True)

class Manager:
    def __init__(self, main_window=None):
        self.app_state = AppState(self)
        self.game_fetcher = GameFetcher()
        self.worker_manager = WorkerManager()
        self.worker_pool = WorkerPool()

        self.signals = ManagerSignals()

    # Called when the load more button is pressed
    @Slot()
    def on_load_more(self):
        logger.info("Loading More")
        self.app_state.clear_grid = False
        self.on_search(load_more=True)

    @Slot(GameCard)
    def on_card_clicked(self, card_widget: GameCard):
        logger.info(f"Card clicked: {card_widget}")
        data = card_widget.get_data
        data.details.system_requirements = self.request_system_req(data.url)

        self.signals.show_game_info_window.emit()
        self.signals.card_clicked.emit(card_widget)

    @Slot(str)
    def on_search_text_changed(self, query: str):
        logger.info(f"Search text changed: {query}")
        self.app_state.search_query = query

    @Slot(bool)
    def on_search(self, load_more: bool = False):
        logger.info("Searching!")

        self.app_state.set_fetch_state = FetchState.FETCHING

        if not load_more:
            self.app_state.clear_grid = True

        self.game_fetch_signals = FetchWorkerSignals()
        self.game_fetch_signals.fetch_finished.connect(self.handle_search_result)

        self.fetch_thread, self.fetch_worker = self.worker_manager.run_in_thread(
            GameFetchWorker(
                self.app_state.search_query,
                self.game_fetcher,
                self.game_fetch_signals,
                load_more,
            )
        )

    @Slot(list)
    def handle_search_result(self, game_data: list[GameData]):
        logger.info("handle_search_result called")

        if not game_data:
            self.app_state.set_fetch_state = FetchState.FETCH_FAIL
            return

        self.app_state.set_fetch_state = FetchState.FETCHED

        self.widgets: list[GameCard] = []

        self.thumb_fetched_signal = ThumbnailWorkerSignals()
        self.thumb_fetched_signal.thumbnail_fetch_finished.connect(
            self.on_thumb_fetched
        )

        for data in game_data:
            card_widget = GameCard(data, on_click=self.on_card_clicked)
            self.widgets.append(card_widget)

            self.thumb_fetch_thread = ThumbnailFetchWorker(card_widget, data.poster_url, self.thumb_fetched_signal)
            self.worker_pool.run_in_thread_pool(self.thumb_fetch_thread)

            self.app_state.game_list.append(data)
        self.signals.cards_ready.emit(self.widgets)

    @Slot(GameCard, bytes)
    def on_thumb_fetched(self, card_widget: GameCard, img_data: bytes):
        data = card_widget.get_data
        if not data:
            return

        if img_data:
            logger.info(f"card {data.title} has thumbnail")
            pixmap = QPixmap()
            pixmap.loadFromData(img_data)
            if not card_widget in self.widgets:
                return

            if not pixmap.isNull():
                card_widget.thumbnail = pixmap
            else:
                logger.info(f"card {data.title}, invalid pixmap, setting default")
                card_widget.thumbnail = get_default_icon()
        else:
            logger.info(f"card {data.title} does not have thumbnail, setting default")
            card_widget.thumbnail = get_default_icon()

    def attempt_download(self, save_path, landing_page_url, progress_callback=None, download_finished_callback=None, provider_btn=None):
        """
        Attempts to download a game from the given landing page URL.
        """
        self.download_worker_signals = DownloadWorkerSignals()
        self.download_worker_signals.download_finished.connect(self.on_download_finished)

        if (progress_callback):
            self.download_worker_signals.progress.connect(progress_callback)

        if (download_finished_callback):
            self.download_worker_signals.download_finished.connect(download_finished_callback)

        provider = DownloaderFactory.get_provider(url=landing_page_url)
        if not provider:
            logger.error(f"no provider found for {landing_page_url}, skipping download")
            return

        direct_link = provider.get_direct_link(landing_page_url)
        if not direct_link:
            logger.error(
                f"direct link not found for {landing_page_url}, skipping download"
            )
            return
        self.start_download(save_path, direct_link, progress_callback, provider_btn)

    def start_download(self, save_path, direct_link, progress_callback=None, provider_btn=None):
        self.download_worker = DownloadWorker(direct_link, save_path, self.download_worker_signals, provider_btn)
        self.worker_manager.run_in_thread(self.download_worker, on_progress=progress_callback)

    def stop_download(self):
        if (hasattr(self, 'download_worker') and self.download_worker):
            self.download_worker.is_cancelled = True
            self.download_worker = None

    @Slot(object)
    def on_download_finished(self, provider):
        for provider_btn in self.app_state.download_queue:
            if provider_btn is provider:
                logger.info(f"Download finished: {provider.landing_page_url}")

                provider_btn.set_downloading_state(is_downloading=False, is_downloaded=True)
                self.app_state.download_queue.remove(provider_btn)
                break

    def cleanup(self):
        self.stop_download()
        self.app_state.download_queue.clear()
        self.app_state.providers.clear()
        self.app_state.game_list.clear()
        self.worker_pool.WORKER_POOL.clear()
        self.worker_manager.cleanup()

    @staticmethod
    def request_filename_from_url(url):
        return get_filename_from_url(url)

    @staticmethod
    def request_provider_name(url: str):
        return get_site_name(url)

    def request_system_req(self, url: str) -> dict[str, str]:
        return self.game_fetcher.get_game_details(url)

    def request_provider_links(self, url: str) -> list[str]:
        return self.game_fetcher.fetch_provder_links(url)
