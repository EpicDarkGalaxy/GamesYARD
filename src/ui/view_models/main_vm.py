from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtWidgets import QWidget

from src.core.utils.log import get_logger

logger = get_logger(__name__)

if TYPE_CHECKING:
    from src.core import AppCoordinator

class MainViewModel(QObject):
    search_state_changed = Signal(str, bool)
    search_finished = Signal(list)
    add_page = Signal(QWidget)
    show_page = Signal(int)

    def __init__(self) -> None:
        super().__init__()
        self.coordinator: "AppCoordinator"

    def initialize(self, coordinator):
        self.coordinator = coordinator
        self.bind_signals()

    def bind_signals(self):
        logger.info("Binding signals")

    @Slot(str)
    def request_search(self, query=""):
        self.coordinator.task_runner.run(
            self.coordinator.model.search_manager.perform_search,
            self._handle_search_result,
            query
            )

    @Slot(list)
    def _handle_search_result(self, games: list):
        self.search_finished.emit(games)

    @Slot(object)
    def _on_close(self, event):
        self.coordinator.model.cleanup()
        event.accept()
