from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtGui import QPixmap

from src.core.aio.workers import Worker
from src.core.utils.log import get_logger

if TYPE_CHECKING:
	from src.core import AppCoordinator, AppCore
	from src.ui.components import GameCard
	from src.ui.views.pages import GameDetailsView

logger = get_logger(__name__)

class GameDetailsViewModel(QObject):
	update_gallery = Signal(list)
	update_sys_req = Signal(dict)
	update_metadata = Signal(dict)

	set_title = Signal(str)
	set_rating = Signal(float, str)
	set_release = Signal(str)
	set_genres = Signal(list)
	set_metacritic = Signal(int, str)
	set_poster = Signal(bytes)

	def __init__(self, model, navigator) -> None:
		super().__init__()
		self.model: "AppCore" = model
		self.nav: object = navigator
		# will be initialized via initialize()
		self.coordinator: "AppCoordinator" | None = None
		# id of the currently viewed game
		self.current_game_id: str | None = None
		self.bind_signals()

	def initialize(self, coordinator):
		self.coordinator = coordinator

	def bind_signals(self):
		pass

	@Slot(dict, str)
	def handle_system_req(self, reqs: dict, game_id: str):
		if self.current_game_id == game_id:
			logger.debug(f"Received and populating system requirements for [{game_id}]")
			self.update_sys_req.emit(reqs)
		else:
			logger.info(f"Received requirements for [{game_id}], but current game is [{self.current_game_id}]. Ignoring.")

	def _get_sys_req(self, game_id: str):
		logger.debug(f"Fetching system requirements for game_id: {game_id}")
		req = Worker(self.model.search_manager.get_system_req, game_id, context=game_id)
		_ = req.signals.result_ready.connect(self.handle_system_req)
		self.model.task_runner.thumb_pool.start(req)

	def _get_gallery(self, game_id: str):
		gall_worker = Worker(self.model.asset_manager.get_screenshots, game_id, context=game_id)
		_= gall_worker.signals.result_ready.connect(self.load_gallery)
		self.model.task_runner.gallery_pool.start(gall_worker)

	@Slot(object)
	def load_card(self, card: "GameCard"):
		if card:
			self.current_game_id = card.id  # The card user is viewing
			title: str = card.title
			rating: float = card.rating
			released: str = card.released
			genres: list[str] = card.genres
			metacritic: int = card.metacritic
			banner: bytes = card.banner

			self.set_title.emit(title)
			self.set_rating.emit(rating, self._get_rating_color(rating))
			self.set_release.emit(released[0])
			self.set_genres.emit(genres)
			self.set_metacritic.emit(metacritic, self._get_metacritic_color(metacritic))
			self.set_poster.emit(banner)
			self._get_gallery(card.id)
			if card.sys_req:
				self.handle_system_req(card.sys_req, card.id)
			else:
				self._get_sys_req(card.id)

	def _get_color(self, value: float=-1, max_val: float=-1) -> str:
		if value and max_val:
			percentage = (value / max_val) * 100
			if percentage >= 75:
				return "#66cc33"  # Green
			elif percentage >= 50:
				return "#ffcc33"  # Yellow
			else:
				return "#ff3333"  # Red

	def _get_rating_color(self, rating: float) -> str:
		return self._get_color(rating, 5.0)

	def _get_metacritic_color(self, score: int) -> str:
		return self._get_color(score, 100.0)

	@Slot(list, str)
	def load_gallery(self, screenshots: list[bytes], game_id: str):
		if self.current_game_id == game_id:
			self.update_gallery.emit(screenshots)
		else:
			logger.info(f"Received screenshots for {game_id}, but current game is {self.current_game_id}. Ignoring.")
