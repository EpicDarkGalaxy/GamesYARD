from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtWidgets import QWidget

from src.core.aio import TaskRunner
from src.core.aio.workers import Worker
from src.core.utils.log import get_logger

logger = get_logger(__name__)

if TYPE_CHECKING:
    from src.core import AppCoordinator, AppCore
    from src.ui.components import GameCard

class MainViewModel(QObject):
    search_state_changed = Signal(str, bool)
    add_page = Signal(QWidget)
    show_page = Signal(int)

    def __init__(self, app_core: "AppCore" , navigator) -> None:
        super().__init__()
        self.app_core = app_core
        self.nav = navigator
        self.coordinator: "AppCoordinator"
        self.cards = {} # {"ID", GameCard}

        self.bind_signals()

    def initialize(self, coordinator):
        self.coordinator = coordinator

    def bind_signals(self):
        logger.info("Binding signals")


    @Slot("GameCard")
    def save_card(self, card: "GameCard"):
        self.cards[card.id] = card
        self.request_thumb(card.id)

    @Slot(str)
    def request_search(self, query=""):
        search_worker = Worker(self.app_core.search_manager.perform_search, query)
        search_worker.signals.result_ready.connect(self._handle_search_result)
        self.app_core.task_runner.run(search_worker)

    @Slot(list)
    def _handle_search_result(self, games: list):
        self.coordinator.forward_search_result(games)

    def request_thumb(self, card_id: str):
        card = self.cards.get(card_id)
        if card:
            thumb_url = card.banner_url
            logger.debug(f"Requesting thumbnail for [{card.title}]")
            thumb_worker = Worker(self.app_core.asset_manager.get_thumbnail, thumb_url, context=card_id)
            thumb_worker.signals.result_ready.connect(self._handle_thumb_result)
        else:
            logger.warning("Can't request for thumbnail, Card was not found")

    @Slot(str, bytes) # 1: ID, 2: img data
    def _handle_thumb_result(self, card_id: str, img_data: bytes):
        card = self.cards.get(card_id)
        logger.debug(f"Recieved thumbnail for ID [{card_id}]")

        if card:
            card.thumbnail = img_data
        else:
            logger.warning(f"MainPresenter: Could not set Thumb, Card ID [{card_id}] was not found.")

    @Slot(object)
    def _on_close(self, event):
        self.app_core.cleanup()
        event.accept()
