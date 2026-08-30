from typing import TYPE_CHECKING

from ..aio.workers import Worker
from ..utils import get_logger, download_icon

if TYPE_CHECKING:
	from ..aio.task_runner import TaskRunner
	from ..services.rawg_service import RawgAPI

logger = get_logger(__name__)

ICON_MAP: dict[str, str] = {
	"steam": "https://upload.wikimedia.org/wikipedia/commons/8/83/Steam_icon_logo.svg",
	"gog": "https://upload.wikimedia.org/wikipedia/commons/2/2f/GOG.com_logo.svg",
	"epic": "https://upload.wikimedia.org/wikipedia/commons/0/07/Epic_Games_logo.svg",
	"ubisoft": "https://upload.wikimedia.org/wikipedia/commons/b/b5/Ubisoft_logo.svg",
	"metacritic": "https://upload.wikimedia.org/wikipedia/commons/2/20/Metacritic.svg",
	"ea": "https://upload.wikimedia.org/wikipedia/commons/e/e0/Electronic_Arts_Logo.svg",
	"xbox": "https://upload.wikimedia.org/wikipedia/commons/f/f9/Xbox_one_logo.svg",
	"playstation": "https://upload.wikimedia.org/wikipedia/commons/0/00/PlayStation_logo.svg",
	"nintendo": "https://upload.wikimedia.org/wikipedia/commons/0/0d/Nintendo_logo.svg",
	"itch": "https://upload.wikimedia.org/wikipedia/commons/d/d1/Itch.io_logo.svg",
}

class AssetManager:
	def __init__(self, task_runner: "TaskRunner", metadata_source: "RawgAPI"):
		super().__init__()
		self.task_runner = task_runner
		self.metadata_source = metadata_source
		self._cache: dict[str, bytes | None] = {}  # {"ID": img_data (bytes)}
		self._icon_cache = {} # {"name or ID": QIcon}

	def get_thumbnail(self, game_id: str, img_url: str):
		if game_id in self._cache:
			logger.debug(f"Returning cached thumbnail for ID: [{game_id}]")
			return self._cache[game_id]

		logger.debug(f"Fetching thumbnail for ID: [{game_id}] from source")
		img_data = self.metadata_source.get_thumbnail(img_url)
		self._cache[game_id] = img_data
		return img_data

	def get_screenshots(self, game_id: str):
		logger.debug(f"Starting Worker for screenshots for id: [{game_id}]")
		shots_data = self.metadata_source.get_game_screenshots(game_id)
		return shots_data


	def get_icon(self, icon_name: str):
		if icon_name in self._icon_cache:
			logger.debug(f"Returning cached icon for: [{icon_name}]")
			return

		icon_url = ICON_MAP.get(icon_name.lower())
		if not icon_url:
			logger.warning(f"No URL found for icon: [{icon_name}]")
			return
