from typing import TYPE_CHECKING
from enum import Enum, auto
from PySide6.QtCore import QObject, Signal, Slot

from ..aio.workers import Worker
from ..utils.log import get_logger

logger = get_logger(__name__)

if TYPE_CHECKING:
    from ..aio.task_runner import TaskRunner
    from ..services.rawg_service import RawgAPI

class SearchState(Enum):
    IDLE = auto()
    SEARCHING = auto()
    COMPLETED = auto()
    ERROR = auto()

class SearchManager(QObject):
    search_completed = Signal(list) # Emits result and state
    search_state_changed = Signal(str, bool)
    search_system_req = Signal(str, dict)

    def __init__(self,task_runner: "TaskRunner", metadata_source: "RawgAPI") -> None:
        super().__init__()
        self._task_runner = task_runner
        self._metadata_source = metadata_source
        self._games_list = []

        self._state = SearchState.IDLE
        self._state_map: dict[SearchState, tuple[str, bool]] = {
            SearchState.IDLE: ("Idle", True),
            SearchState.SEARCHING: ("Searching", False),
            SearchState.COMPLETED: ("Completed", True),
            SearchState.ERROR: ("Error", True)
        }

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value: SearchState):
        self._state = value
        result = self._state_map.get(self._state)
        if result:
            text, is_running = result
            self.search_state_changed.emit(text, is_running)

    def perform_search(self, query: str="", loadmore: bool=False):
        logger.debug(f"Starting Search Worker for [{query}], loadmore: [{loadmore}]")
        search_worker = Worker(self._metadata_source.search_games, query)
        search_worker.signals.result_ready.connect(self._handle_search_result)
        self._task_runner.run(search_worker)
        self.state = SearchState.SEARCHING

    @Slot(list)
    def _handle_search_result(self, games):
        logger.debug(f"Search Worker finished with Results [{len(games)}]")
        self._games_list.append(games)
        self.state = SearchState.COMPLETED if len(games) > 0 else SearchState.ERROR
        self.search_completed.emit(games)



    def get_system_req(self, game_id: str):
        logger.debug(f"Starting System Requirement Worker for id: [{game_id}]")
        req_worker = Worker(self._metadata_source.get_game_system_requirements, game_id, context=game_id)
        req_worker.signals.result_ready.connect(self._handle_system_req_result)
        self._task_runner.run(req_worker)

    @Slot(object, object)
    def _handle_system_req_result(self, req: dict, game_id: str):
        self.search_system_req.emit(game_id, req)
