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

        self.download_manager.stop_all_downloads()
        self.task_runner.pool.clear()

        if event:
            event.accept()

        import os

        os._exit(0)
