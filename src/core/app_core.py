import os

import dotenv
from PySide6.QtCore import QObject

from ..core.aio import TaskRunner
from .managers import DownloadManager, AssetManager, SearchManager
from .services.rawg_service import RawgAPI
from .signals import Signals
from .utils import get_logger

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

dotenv.load_dotenv()

class AppCore(QObject):
    def __init__(self):
        super().__init__()
        self.app_state = AppState(self)

        self.task_runner = TaskRunner()

        self.rawg_api = RawgAPI(api_key=os.getenv("RAWG_API_KEY", "")) # Use your RAWG api

        self.download_manager = DownloadManager(self.task_runner)
        self.search_manager = SearchManager(self.task_runner, self.rawg_api)
        self.asset_manager = AssetManager(self.task_runner, self.rawg_api)

        self.signals = Signals()
        self.download_signals = Signals()

    def cleanup(self, event=None):
        logger.info("AppCore cleanup starting...")

        self.download_manager.stop_all_downloads()
        self.task_runner.pool.clear()

        if event:
            event.accept()

        import os
        os._exit(0)
