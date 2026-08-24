from PySide6.QtCore import QObject

from ..core.aio import TaskRunner
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
        logger.info(f"Setting opened card to: {card.get_id}")
        self._opened_card = card
        self._manager.signals.opened_card_changed.emit(card)

class AppCore(QObject):
    def __init__(self):
        super().__init__()
        self.app_state = AppState(self)
        self.game_fetcher = GameFetcher()

        self.task_runner = TaskRunner()

        self.download_manager = DownloadManager(self.task_runner)
        self.search_manager = SearchManager(self.task_runner)
        self.thumbnail_manager = ThumbnailManager(self.task_runner)

        self.signals = Signals()
        self.download_signals = Signals()

    def cleanup(self, event=None):
        logger.info("AppCore cleanup starting...")

        self.download_manager.stop_all_downloads()
        self.task_runner.pool.clear()

        if event:
            event.accept()

        # 1. Stop all workers in managers
        self.download_manager.stop_all_downloads()

        # 2. Force the ThreadPool to wait (or discard)
        # This is the secret sauce for clean exits
        self.task_runner.pool.clear()

        # 3. If the user provided an event, accept it so the window closes
        if event:
            event.accept()

        # 4. Optional: Force exit to ensure no "ghost" threads survive
        import os
        os._exit(0)
