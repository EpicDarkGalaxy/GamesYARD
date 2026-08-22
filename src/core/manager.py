from enum import Enum

from PySide6.QtCore import QObject, Slot

from src.core.downloaders import DownloaderFactory
from src.core.tools.utils import get_default_icon, get_filename_from_url, get_site_name

from ..core.aio import (
    DownloadWorker,
    GameFetchWorker,
    ThumbnailFetchWorker,
    WorkerManager,
    LinkExtractionWorker,
    WorkerPool,
)
from ..core.models import GameData
from ..ui import ManagerSignals, DownloadSignals
from .tools import GameFetcher, get_logger

logger = get_logger(__name__)

class FetchState(Enum):
    READY = 1
    FETCHING = 2
    FETCHED = 3
    FETCH_FAIL = 4

class Download:
    def __init__(self, save_path, download_url, landing_page_url, manager=None):
        self.save_path = save_path
        self.download_url = download_url
        self.landing_page_url = landing_page_url
        self.download_progress = 0
        self.manager = manager

    def update_progress(self, progress):
        logger.info(f"Download progress: {progress}")
        self.download_progress = progress
        if self.manager:
            self.manager.download_signals.download_progress.emit(self.download_progress)

class AppState:
    def __init__(self, manager):
        self.manager = manager
        self.last_search_query = "" # Used when user clicks load more button
        self._fetch_state = FetchState.READY
        self._opened_card = None # Card That user is currently viewing
        self.clear_grid = False  # Whether the grid should be cleared before fetching
        self.is_downloading = False
        self.download_queue = []
        self.game_list: list[GameData] = []  # List of games fetched from internet

    @property
    def get_opened_card(self):
        return self._opened_card

    @get_opened_card.setter
    def set_opened_card(self, card):
        self._opened_card = card
        self.manager.signals.opened_card_changed.emit(card)

    @property
    def get_fetch_state(self) -> FetchState:
        return self._fetch_state

    @get_fetch_state.setter
    def set_fetch_state(self, state: FetchState):
        self._fetch_state = state
        if (self._fetch_state is FetchState.READY):
            self.manager.signals.update_fetch_btn.emit(f"Ready", True)
        elif (self._fetch_state is FetchState.FETCHING):
            self.manager.signals.update_fetch_btn.emit("Fetching", False)
        elif (self._fetch_state is FetchState.FETCHED):
            self.manager.signals.update_fetch_btn.emit("Fetched", True)
        elif (self._fetch_state is FetchState.FETCH_FAIL):
            self.manager.signals.update_fetch_btn.emit("Fetch Fail", True)

class Manager(QObject):
    def __init__(self):
        super().__init__()
        self.app_state = AppState(self)
        self.game_fetcher = GameFetcher()

        # Even though WorkerManager should handle WorkerPool,
        # but they both are not in any kind of relationship :)
        self.worker_manager = WorkerManager()
        self.worker_pool = WorkerPool()

        self.signals = ManagerSignals()
        self.download_signals = DownloadSignals()


    # Called when the load more button is pressed
    def load_more(self):
        logger.info("Loading More")
        self.app_state.clear_grid = False
        self.search(self.app_state.last_search_query, load_more=True)

    def search(self, query: str, load_more: bool = False):
        logger.info("Searching!")

        if not load_more:
            self.app_state.last_search_query = query
            self.app_state.clear_grid = True

        self.app_state.set_fetch_state = FetchState.FETCHING

        self.fetch_thread, self.fetch_worker = self.worker_manager.run_in_thread(
            GameFetchWorker(
                query,
                self.game_fetcher,
                load_more,
            )
        )
        self.fetch_worker.signals.fetch_finished.connect(self.handle_search_result)

    @Slot(list)
    def handle_search_result(self, game_data: list[GameData]):
        logger.info("handle_search_result called")

        if not game_data:
            self.app_state.set_fetch_state = FetchState.FETCH_FAIL
            return

        self.app_state.set_fetch_state = FetchState.FETCHED


        self.app_state.game_list = game_data
        self.signals.cards_ready.emit(game_data, self.app_state.clear_grid)

    def request_thumbnail(self, id, img_url):
        logger.info(f"Starting Worker for thumbnail for url {img_url}")
        thumbnail_worker = ThumbnailFetchWorker(id, img_url)
        thumbnail_worker.signals.thumbnail_fetch_finished.connect(self.thumb_fetched)
        self.worker_pool.run_in_thread_pool(thumbnail_worker)

    @Slot(str, bytes)
    def thumb_fetched(self, id, img_data: bytes):
        logger.info(f"Thumbnail Worker finished for card {id}")
        self.signals.thumb_fetched.emit(id, img_data)

    def attempt_download(self, save_path, landing_page_url):
        """
        Attempts to download a game from the given landing page URL.
        """

        provider = DownloaderFactory.get_provider(url=landing_page_url)
        if not provider:
            logger.error(f"no provider found for {landing_page_url}, skipping download")
            return

        download = Download(save_path, "", landing_page_url=landing_page_url, manager=self)
        self.app_state.download_queue.append(download)

        self.link_worker = LinkExtractionWorker(provider.get_method(), landing_page_url, provider)
        self.link_worker.signals.link_extracted.connect(self.on_download_url)
        self.worker_manager.run_in_thread(self.link_worker)

    def on_download_url(self, download_url, landing_page_url):
        logger.info(f"Link extracted: {download_url}")

        for download in self.app_state.download_queue:
            if download.landing_page_url == landing_page_url:
                download.download_url = download_url
                self.start_download(download)
                break

    def start_download(self, download: Download):
        logger.info(f"Starting download: {download.download_url} to {download.save_path}")

        self.download_worker = DownloadWorker(download.download_url, download.save_path)
        self.download_worker.signals.download_finished.connect(self.on_download_finished)
        self.worker_manager.run_in_thread(self.download_worker, on_progress=download.update_progress)
        self.app_state.download_queue.append(download)
        self.app_state.is_downloading = True

    def stop_download(self):
        # Later, we will use a list containing the deployed workers
        if (hasattr(self, 'download_worker') and self.download_worker):
            self.download_worker.is_cancelled = True
            self.download_worker = None

    def on_download_finished(self, provider):
        logger.info(f"Download finished: {provider.landing_page_url}")

        for provider_btn in self.app_state.download_queue:
            if provider_btn is provider:
                logger.info(f"Removing provider from download queue: {provider.landing_page_url}")

                provider_btn.set_downloading_state(is_downloading=False, is_downloaded=True)
                self.app_state.download_queue.remove(provider_btn)
                break
        if (not self.app_state.download_queue):
            self.app_state.is_downloading = False

    def cleanup(self, event=None):
        self.stop_download()
        self.app_state.download_queue.clear()
        self.app_state.game_list.clear()
        self.worker_pool.WORKER_POOL.clear()
        self.worker_manager.cleanup()
        self.signals.shutting_down.emit()
        if (event):
            logger.info("Cleaning up and exiting...")
            event.accept()

    @staticmethod
    def request_filename_from_url(url):
        return get_filename_from_url(url)

    @staticmethod
    def request_default_icon():
        return get_default_icon()

    @staticmethod
    def request_provider_name(url: str):
        return get_site_name(url)

    def request_system_req(self, url: str) -> dict[str, str]:
        return self.game_fetcher.get_game_details(url)

    def request_provider_links(self, url: str) -> list[str]:
        return self.game_fetcher.fetch_provder_links(url)
