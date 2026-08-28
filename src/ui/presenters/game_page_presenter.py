from typing import TYPE_CHECKING
from PySide6.QtCore import SIGNAL, Slot
from PySide6.QtGui import QPixmap
from ...core.utils.log import get_logger

if TYPE_CHECKING:
	from src.core import AppCore
	from ..views.pages.details_page import GameDetailsView
	from ..components import GameCard

logger = get_logger(__name__)

class GamePagePresenter:
	def __init__(self, view: "GameDetailsView", model: "AppCore") -> None:
		self.view = view
		self.model = model
		self.current_game_id: str

		self.bind_signals()

	def bind_signals(self):
		# View

		# Model
		self.model.search_manager.search_system_req.connect(self._handle_system_req)
		self.model.asset_manager.screenshots_ready.connect(self.load_gellery)
		self.model.asset_manager.icon_ready.connect(lambda icon_path: logger.info(f"Icon Received({icon_path})"))

	@Slot(str, dict)
	def _handle_system_req(self, game_id: str, reqs: dict[str, str]):
		if self.current_game_id == game_id:
			logger.debug(f"Received and populating system requirements for [{game_id}]")
			self.view.populate_requirements(reqs, game_id)
		else:
			logger.info(f"Received requirements for [{game_id}], but current game is [{self.current_game_id}]. Ignoring.")

	def load_card(self, card: "GameCard"):
		if card:
			self.current_game_id = card.id # The card user is viewing
			title = card.title
			rating = card.rating
			released = card.released,
			genres = card.genres
			metacritic = card.metacritic
			banner = card.banner

			self.view.set_title(title)
			self.view.set_rating(rating, self._get_rating_color(rating))
			self.view.set_release(released[0])
			self.view.set_genres(genres)
			self.view.set_metacritic(metacritic, self._get_metacritic_color(metacritic))
			self.view.set_poster(banner)
			self.model.asset_manager.get_screenshots(card.id)
			if card.sys_req:
				self._handle_system_req(card.id, card.sys_req)
			else:
				self.model.search_manager.get_system_req(card.id)

	def _get_color(self, value: float, max_val: float) -> str:
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

	@Slot(str, list)
	def load_gellery(self, game_id: str, screenshots: list[bytes]):
		if self.current_game_id == game_id:
			self.view.update_gallery(screenshots)
		else:
			logger.info(f"Received screenshots for {game_id}, but current game is {self.current_game_id}. Ignoring.")
