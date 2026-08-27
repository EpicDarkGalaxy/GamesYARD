from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, Signal, Slot
from ..tools.log import get_logger
from ..aio.workers import Worker

if TYPE_CHECKING:
	from ..aio.task_runner import TaskRunner
	from ..fetchers.rawg_api import RawgApiFetcher

logger = get_logger(__name__)

class ThumbnailManager(QObject):
	thumb_ready = Signal(str, bytes)

	def __init__(self, task_runner: "TaskRunner", metadata_source: "RawgApiFetcher"):
		super().__init__()
		self.task_runner = task_runner
		self.metadata_source = metadata_source
		self._cache = {} # {"ID", img_data (bytes)}

	def get_thumb(self, game_id: str, img_url: str):
		logger.debug(f"Starting Worker for thumbnail for URL: [{img_url}] of ID: [{game_id}]")
		thumb_worker = Worker(self.metadata_source.get_thumbnail, img_url, context=game_id)
		thumb_worker.signals.result_ready.connect(self._handle_thumb_fetched)
		self.task_runner.run(thumb_worker)

	@Slot(bytes, str)
	def _handle_thumb_fetched(self, img_data: bytes, game_id: str):
		logger.debug(f"Thumbnail Worker finished for id: [{game_id}]")
		self.thumb_ready.emit(game_id, img_data)
		