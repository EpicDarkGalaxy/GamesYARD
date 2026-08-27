from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, Signal, Slot

from ..aio.workers import Worker
from ..tools.log import get_logger

logger = get_logger(__name__)

if TYPE_CHECKING:
    from ..aio.task_runner import TaskRunner
    from ..fetchers.rawg_api import RawgApiFetcher

class SearchManager(QObject):
    search_completed = Signal(list)

    def __init__(self,task_runner: "TaskRunner", metadata_source: "RawgApiFetcher") -> None:
        super().__init__()
        self.task_runner = task_runner
        self.metadata_source = metadata_source

    def search(self, query: str="", loadmore: bool=False):
        logger.debug(f"SearchManager: Search requested for [{query}], loadmore: [{loadmore}]")
        search_worker = Worker(self.metadata_source.search_games, query)
        search_worker.signals.result_ready.connect(self._handle_search_result)
        self.task_runner.run(search_worker)

    @Slot(list)    
    def _handle_search_result(self, games):
        logger.debug(f"SearchManager: Search finished with Results [{len(games)}]")
        self.search_completed.emit(games)
        
