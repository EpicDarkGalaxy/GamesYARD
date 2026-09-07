import os

import dotenv
from typing_extensions import final

from src.core.aio import TaskRunner
from src.core.managers import AssetManager, DownloadManager, SearchManager
from src.core.services.metadata import RawgAPI
from src.core.utils import get_logger

logger = get_logger(__name__)
dotenv.load_dotenv()

@final
class AppCore:
    """
    Core service locator and state container.
    Manages background infrastructure (TaskRunner, DownloadManager, metadata APIs)
    independently of any UI or routing logic.
    """
    def __init__(self):
        self.rawg_api: RawgAPI = RawgAPI(
            api_key=os.getenv("RAWG_API_KEY", "")
        )  # Use your RAWG API KEY
        self.task_runner = TaskRunner()
        self.download_manager = DownloadManager(self.task_runner)
        self.search_manager = SearchManager(self.rawg_api)
        self.asset_manager: AssetManager = AssetManager(self.rawg_api)

    def cleanup(self, event=None):
        logger.info("AppCore cleanup starting...")

        # Stop downloads and clear worker pool
        try:
            self.download_manager.stop_all_downloads()
        except Exception as e:
            logger.warning(f"Error stopping downloads during cleanup: {e}")

        # Attempt to wait briefly for the thread pool to finish
        try:
            # QThreadPool.waitForDone expects milliseconds
            self.task_runner.pool.waitForDone(3000)  # wait up to 3s
        except Exception:
            logger.debug("task_runner.pool.waitForDone not available/failed")

        if event:
            try:
                event.accept()
            except Exception:
                logger.debug("event.accept() failed during cleanup")

        logger.info("AppCore cleanup finished; returning to caller for process exit.")
