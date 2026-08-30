<<<<<<< HEAD
from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtGui import QPixmap

from src.core.aio.workers import Worker
from src.core.utils import get_logger

if TYPE_CHECKING:
 from src.core.app_coordinator import AppCoordinator
=======
from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtGui import QPixmap
from ...core.utils import get_logger
from typing import TYPE_CHECKING
from ...core.aio.workers import Worker

if TYPE_CHECKING:
 from ...core.app_coordinator import AppCoordinator
>>>>>>> 49411a3e9ffa7ace8a740fca7c33696c699c18bc

logger = get_logger(__name__)

class SearchCatalogViewModel(QObject):
	update_grid = Signal(list)

	def __init__(self, model, navigator) -> None:
		super().__init__()
		self.model = model
		self.coordinator: "AppCoordinator"
		self.nav = navigator
		self.cards = {}

	def initialize(self, coordinator):
		self.coordinator = coordinator

	def save_card(self, card):
		self.cards[card.id] = card

	def add_to_grid(self, games):
		logger.debug(f"Received games [{len(games)}]")
		if games:
			self.update_grid.emit(games)

	def _handle_card_click(self, card):
		logger.debug(f"Card clicked: {card}")
		self.coordinator.forward_card(card)
		self.nav.go_to("details")

	def get_thumb(self, card_id: str, url: str):
		logger.debug(f"Fetching thumbnail for card: {card_id} from {url}")
		thumb_worker = Worker(self.model.asset_manager.get_thumbnail, card_id, url, context=card_id)
		_ = thumb_worker.signals.result_ready.connect(self._handle_thumb_result)
		self.model.task_runner.run(thumb_worker)

	@Slot(dict, str)
	def _handle_thumb_result(self, img_data, card_id):
		logger.debug(f"Handle thumbnail result for card {card_id}: data type {type(img_data)}")

		card = self.cards.get(card_id)
		if card and img_data:
			logger.debug(f"Thumbnail loading for card: {card_id}")
			card.thumbnail = img_data
		else:
			logger.warning(f"Failed to load thumbnail for card: {card_id}")
