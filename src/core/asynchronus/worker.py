from PySide6.QtCore import QObject, QThread, Slot

from ..fetcher import GameFetcher
from ..log import get_logger
from ..signals import FetchWorkerSignals

logger = get_logger(__name__)

class WorkerManager:

    @staticmethod
    def run_in_thread(worker, on_finish=None, on_fail=None):
        thread = QThread()
        worker.moveToThread(thread)

        thread.started.connect(worker.run)

        if (on_fail): worker.signals.fetch_fail.connect(on_fail)
        if (on_finish): worker.signals.fetch_finished.connect(on_finish)

        def cleanup():
            thread.quit()
            thread.wait()
            worker.deleteLater()
            thread.deleteLater()

        worker.signals.finished.connect(cleanup)
        thread.start()
        return thread, worker

class GameFetchWorker(QObject):
    def __init__ (self, search_query: str, game_fetcher: GameFetcher, signals):
        super().__init__()
        self.search_query = search_query
        self.game_fetcher = game_fetcher
        self.signals = signals

    @Slot()
    def run(self):
        cards_list = self.game_fetcher.get_game_list(self.search_query)
        self.signals.fetch_finished.emit(cards_list)
        self.signals.finished.emit()
