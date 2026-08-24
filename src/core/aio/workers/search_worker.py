from typing import TYPE_CHECKING

from ..base_worker import BaseWorker
from ..worker_signals import SearchWorkerSignals

if TYPE_CHECKING:
    from ...tools.fetcher import GameFetcher


class SearchWorker(BaseWorker):
    def __init__ (self, search_query: str, game_fetcher: "GameFetcher", load_more:bool=False):
        super().__init__()
        self.search_query = search_query
        self.game_fetcher = game_fetcher
        self.load_more = load_more
        self.signals = SearchWorkerSignals()

    def run(self):
        cards_list = self.game_fetcher.get_game_list(self.search_query, self.load_more)
        self.signals.search_finished.emit(cards_list)
