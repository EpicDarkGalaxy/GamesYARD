from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, Signal, Slot

from src.core.utils.log import get_logger

logger = get_logger(__name__)

if TYPE_CHECKING:
    from src.core import AppCore, AppCoordinator

class HomeCatalogViewModel(QObject):
    card_clicked = Signal(object)

    set_heros = Signal(list)
    set_trending = Signal(list)
    set_newest = Signal(list)
    set_best_rated = Signal(list)

    def __init__(self) -> None:
        super().__init__()
        self.coordinator: AppCoordinator

    def initialize(self, coordinator):
        self.coordinator = coordinator
        self.init_home()

    def init_home(self):
        self.get_home_catalog()

    def get_home_catalog(self):
        logger.info("Fetching home catalog...")
        self.coordinator.task_runner.run(
            self.coordinator.model.search_manager.get_home_catalog, 
            self._handle_home_catalog
            )

    @Slot(dict)
    def _handle_home_catalog(self, catalog: dict):
        heros = catalog.get("featured")
        trending = catalog.get("trending")
        newest = catalog.get("newest")
        best_rated = catalog.get("best_rated")

        self.set_trending.emit(trending)
        self.set_heros.emit(heros)
        self.set_best_rated.emit(best_rated)
        self.set_newest.emit(newest)

    def _handle_card_click(self, game_data):
        self.card_clicked.emit(game_data)
        self.coordinator.navigate("details")
