from PySide6.QtCore import QObject, Signal, Slot
from enum import Enum, auto
from typing import TYPE_CHECKING

from ..models import GameData

from ..aio.worker import SearchWorker
from ..tools.log import get_logger
from ..tools.fetcher import GameFetcher

logger = get_logger(__name__)


if TYPE_CHECKING:
    from ..aio.worker import WorkerManager


class SearchState(Enum):
    READY = auto()
    FETCHING = auto()
    FETCHED = auto()
    FETCH_FAIL = auto()

    @property
    def ui_info(self) -> tuple[str, bool]:
        return {
            SearchState.READY: ("Ready", True),
            SearchState.FETCHING: ("Fetching", False),
            SearchState.FETCHED: ("Fetched", True),
            SearchState.FETCH_FAIL: ("Fetch Fail", True),
        }[self]

class SearchManager(QObject):
    search_completed = Signal(list, bool)
    search_state_changed = Signal(str, bool)

    def set_search_state(self, state: SearchState):
        label, enabled = state.ui_info
        self.search_state_changed.emit(label, enabled)

    def __init__(self, worker_manager: "WorkerManager"):
        super().__init__()
        self.last_search_query = ""
        self.temp_load_more = False

        self.worker_manager = worker_manager
        self.game_fetcher = GameFetcher()


    def search(self, query, load_more=False):
        self.temp_load_more = not load_more
        print(f"Searching for: {query}, load_more: {load_more}")

        if not load_more:
            self.last_search_query = query

        self.set_search_state(SearchState.FETCHING)

        self.fetch_thread, self.fetch_worker = self.worker_manager.run_in_thread(
            SearchWorker(
                query,
                self.game_fetcher,
                load_more,
            )
        )
        self.fetch_worker.signals.fetch_finished.connect(self.handle_search_result)

    def load_more(self):
        logger.info("Loading More")
        self.search(self.last_search_query, load_more=True)

    @Slot(list)
    def handle_search_result(self, games: list[GameData]):
        logger.info("handle_search_result called")

        if not games:
            self.set_search_state(SearchState.FETCH_FAIL)
            return

        self.set_search_state(SearchState.FETCHED)
        self.search_completed.emit(games, self.temp_load_more)
