from curl_cffi import get
from PySide6.QtCore import Signal, Slot
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFileDialog

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
from ..core.models import GameData, GameDetails
from ..ui.ui_signals import GameInfoWindowSignals, UiSignals
from ..ui.widget import GameCardWidget
from .tools import GameFetcher, get_default_icon, get_logger

logger = get_logger(__name__)


class AppState:
    def __init__(self):
        self.search_query = ""
        self.clear_grid = False
        self.game_list: list[GameData] = []


class _Manager:
    def __init__(self):
        self.app_state = AppState()
        self.game_fetcher = GameFetcher()
        self.worker_manager = WorkerManager()
        self.worker_pool = WorkerPool()
        self.main_window = None

        self.game_info_signals = GameInfoWindowSignals()

    # Called when the load more button is pressed
    @Slot()
    def on_load_more(self):
        logger.info("Loading More")
        self.app_state.clear_grid = False
        self.on_search(load_more=True)

    @Slot(GameCardWidget)
    def on_card_clicked(self, card_widget: GameCardWidget):
        from src.ui.windows.game_info_window import GameInfoWindow

        logger.info(f"Card clicked: {card_widget}")
        data = card_widget.get_data
        data.details.system_requirements = self.request_system_req(data.url)

        self.game_info_signals.request_show_window.emit(GameInfoWindow())
        self.game_info_signals.game_selected.emit(data)

    @Slot(str)
    def on_search_text_changed(self, query: str):
        logger.info(f"Search text changed: {query}")
        self.app_state.search_query = query

    @Slot(bool)
    def on_search(self, load_more: bool = False):
        logger.info("on_search pressed!")

        self.main_window.update_fetch_btn("Fetching...", False)

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
    def handle_search_result(self, game_data):
        logger.info("handle_search_result called")

        if not game_data:
            self.main_window.update_fetch_btn("Failed", True)
            return

        self.main_window.update_fetch_btn("Fetched", True)
        self.widgets: list[GameCardWidget] = []

        self.thumb_fetched_signal = ThumbnailWorkerSignals()
        self.thumb_fetched_signal.thumbnail_fetch_finished.connect(
            self.on_thumb_fetched
        )

        for data in game_data:
            card_widget = GameCardWidget(data, on_click=self.on_card_clicked)
            self.widgets.append(card_widget)

            self.thumb_fetch_thread = ThumbnailFetchWorker(
                card_widget, data.poster_url, self.thumb_fetched_signal
            )
            self.worker_pool.run_in_thread_pool(self.thumb_fetch_thread)

            self.app_state.game_list.append(data)
        self.main_window.append_to_grid(self.widgets)

    @Slot(GameCardWidget, bytes)
    def on_thumb_fetched(self, card_widget: GameCardWidget, img_data: bytes):
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

    def store_main_window(self, window):
        """
        Stores the MainWindow if it is not an imposter.
        Its a one-time operation.

        Args:
            window: The main window to store.

        """
        if not self.main_window:  # We don't want to store imposters
            logger.info(f"Storing main window: {window}")
            self.main_window = window
        else:
            logger.error("No Main Window was provided, or its an imposter")

    def resolve_and_download(self, save_path, landing_page_url, progress_callback=None):
        self.progress_signal = DownloadWorkerSignals()
        self.progress_signal.progress.connect(progress_callback)

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
        self.start_download(save_path, direct_link, progress_callback)

    def start_download(self, save_path, direct_link, progress_callback=None):
        self.download_worker = DownloadWorker(
            direct_link, save_path, self.progress_signal
        )
        self.worker_manager.run_in_thread(
            self.download_worker, on_progress=progress_callback
        )

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


MANAGER = _Manager()
