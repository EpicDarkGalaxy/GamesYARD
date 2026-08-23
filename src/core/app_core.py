
from PySide6.QtCore import QObject, Slot

from src.core.tools.utils import get_default_icon, get_filename_from_url, get_site_name

from ..core.aio import (
    WorkerManager,
    WorkerPool,
)
from ..core.models import GameData
from .managers import DownloadManager, SearchManager, ThumbnailManager
from .signals import Signals
from .tools import GameFetcher, get_logger

logger = get_logger(__name__)

class AppState:
    def __init__(self, manager):
        self._manager = manager
        self._opened_card = None # The card That user is currently viewing

    @property
    def get_opened_card(self):
        return self._opened_card

    @get_opened_card.setter
    def set_opened_card(self, card):
        self._opened_card = card
        self._manager.signals.opened_card_changed.emit(card)

class AppCore(QObject):
    def __init__(self):
        super().__init__()
        self.app_state = AppState(self)
        self.game_fetcher = GameFetcher()

        # Even though WorkerManager should handle WorkerPool,
        # but they both are not in any kind of relationship :)
        self.worker_pool = WorkerPool()
        self.worker_manager = WorkerManager()

        self.download_manager = DownloadManager(self.worker_manager)
        self.search_manager = SearchManager(self.worker_manager)
        self.thumbnail_manager = ThumbnailManager(self.worker_pool)

        self.signals = Signals()
        self.download_signals = Signals()


    def cleanup(self, event=None):
        self.download_manager.stop_download()
        self.worker_pool.WORKER_POOL.clear()
        self.worker_manager.cleanup()
        self.signals.shutting_down.emit()
        if (event):
            logger.info("Cleaning up and exiting...")
            event.accept()
