from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtGui import QIcon

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

class AssetManager(QObject):
    thumb_ready = Signal(str, bytes)
    screenshots_ready = Signal(str, list)
    icon_ready = Signal(QIcon)

    def __init__(self, task_runner: "TaskRunner", metadata_source: "RawgAPI"):
        super().__init__()
        self.task_runner = task_runner
        self.metadata_source = metadata_source
        self._cache = {}  # {"ID": img_data (bytes)}
        self._icon_cache = {} # {"name or ID": QIcon}

    def get_thumbnail(self, game_id: str, img_url: str):
        if game_id in self._cache:
            logger.debug(f"Returning cached thumbnail for ID: [{game_id}]")
            self.thumb_ready.emit(game_id, self._cache[game_id])
            return

        logger.debug(
            f"Starting Worker for thumbnail for URL: [{img_url}] of ID: [{game_id}]"
        )
        thumb_worker = Worker(
            self.metadata_source.get_thumbnail, img_url, context=game_id
        )
        thumb_worker.signals.result_ready.connect(self._on_thumb_ready)
        self.task_runner.run(thumb_worker)

    @Slot(bytes, str)
    def _on_thumb_ready(self, img_data: bytes, game_id: str):
        logger.debug(f"Thumbnail Worker finished for id: [{game_id}]")
        self._cache[game_id] = img_data
        self.thumb_ready.emit(game_id, img_data)

    def get_screenshots(self, game_id: str):
        logger.debug(f"Starting Worker for screenshots for id: [{game_id}]")
        ss_worker = Worker(self.metadata_source.get_game_screenshots, game_id, context=game_id)
        _ = ss_worker.signals.result_ready.connect(self._on_screenshots_ready)
        self.task_runner.run(ss_worker)

    @Slot(list, str)
    def _on_screenshots_ready(self, shots: list, game_id: str):
        logger.debug(f"Screenshot Worker finished for id: [{game_id}]")
        self.screenshots_ready.emit(game_id, shots)

    def get_icon(self, icon_name: str):
        if icon_name in self._icon_cache:
            logger.debug(f"Returning cached icon for: [{icon_name}]")
            self.icon_ready.emit(self._icon_cache[icon_name])
            return

        icon_url = ICON_MAP.get(icon_name.lower())
        if not icon_url:
            logger.warning(f"No URL found for icon: [{icon_name}]")
            return

        logger.debug(f"Starting Worker for icon: [{icon_name}] at URL: [{icon_url}]")
        icon_worker = Worker(download_icon, icon_url, context=icon_name)
        _ = icon_worker.signals.result_ready.connect(self._on_icon_ready)
        self.task_runner.run(icon_worker)

    @Slot(QIcon, str)
    def _on_icon_ready(self, icon: QIcon, icon_name: str):
        logger.debug(f"Icon Worker finished for: [{icon_name}]")
        self._icon_cache[icon_name] = icon
        self.icon_ready.emit(icon)
