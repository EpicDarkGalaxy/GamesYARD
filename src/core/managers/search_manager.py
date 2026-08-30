from enum import Enum, auto
<<<<<<< HEAD
from typing import TYPE_CHECKING
=======
>>>>>>> 49411a3e9ffa7ace8a740fca7c33696c699c18bc

from src.core.aio.workers import Worker
from src.core.utils import get_logger

logger = get_logger(__name__)

if TYPE_CHECKING:
    from src.core.aio import TaskRunner
    from src.core.services import RawgAPI

class SearchState(Enum):
    IDLE = auto()
    SEARCHING = auto()
    COMPLETED = auto()
    ERROR = auto()

class SearchManager:
    def __init__(self,task_runner: "TaskRunner", metadata_source: "RawgAPI") -> None:
        super().__init__()
        self._task_runner = task_runner
        self._metadata_source = metadata_source
        self._games_list = []
        self._game_reqs = {}

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

    def perform_search(self, query: str="", loadmore: bool=False):
        logger.debug(f"Searching for [{query}], loadmore: [{loadmore}]")

        return(self._metadata_source.search_games(query))

    def get_system_req(self, game_id: str) -> dict[str, str]:
        # Check cache first
        if game_id in self._game_reqs:
            logger.debug(f"Returning cached requirements for: [{game_id}]")
            return self._game_reqs[game_id]

        req: dict[str, str] = self._metadata_source.get_game_system_requirements(game_id)

        # Store in cache
        self._game_reqs[game_id] = req
<<<<<<< HEAD
        return req
=======
        return req
>>>>>>> 49411a3e9ffa7ace8a740fca7c33696c699c18bc
