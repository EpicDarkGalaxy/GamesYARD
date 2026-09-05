from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, Signal, Slot

from src.core.aio.workers import Worker
from src.core.utils import get_logger

if TYPE_CHECKING:
 from src.core.app_coordinator import AppCoordinator

logger = get_logger(__name__)

class SearchCatalogViewModel(QObject):
	update_grid = Signal(list)
	card_clicked = Signal(object)

	def __init__(self) -> None:
		super().__init__()
		self.coordinator: "AppCoordinator"

	def initialize(self, coordinator):
		self.coordinator = coordinator

	def add_to_grid(self, games):
		logger.debug(f"Received games [{len(games)}]")
		if games:
			self.update_grid.emit(games)

	def _handle_card_click(self, card):
		logger.debug(f"Card clicked: {card}")
		self.coordinator.navigate("details")
		self.card_clicked.emit(card)

	def _handle_search_catalog_hide(self):
		logger.debug("Search catalog hidden")
		self.coordinator.task_runner.pool.clear()
