from curl_cffi import requests as r

from PySide6.QtCore import QObject, QThread, Slot

from ..tools import GameFetcher, get_logger

logger = get_logger(__name__)

class WorkerManager:

    @staticmethod
    def run_in_thread(worker, on_finish=None, on_fail=None, on_progress=None):
        thread = QThread()
        worker.moveToThread(thread)

        thread.started.connect(worker.run)

        if (on_fail): worker.signals.fetch_fail.connect(on_fail)
        if (on_finish): worker.signals.fetch_finished.connect(on_finish)
        if (on_progress): worker.signals.progress.connect(on_progress)

        def cleanup():
            thread.quit()
            thread.wait()
            worker.deleteLater()
            thread.deleteLater()

        worker.signals.finished.connect(cleanup)
        worker.signals.fail.connect(cleanup)

        thread.start()
        return thread, worker

class GameFetchWorker(QObject):
    def __init__ (self, search_query: str, game_fetcher: GameFetcher, signals, load_more:bool=False):
        super().__init__()
        self.search_query = search_query
        self.game_fetcher = game_fetcher
        self.signals = signals
        self.load_more = load_more

    @Slot()
    def run(self):
        cards_list = self.game_fetcher.get_game_list(self.search_query, self.load_more)
        self.signals.fetch_finished.emit(cards_list)
        self.signals.finished.emit()

class DownloadWorker(QObject):
    def __init__(self, url: str, save_path: str, signals):
        super().__init__()
        self.url = url
        self.save_path = save_path
        self.signals = signals

    @Slot()
    def run(self):
        try:
            # For now, i am keeping the download logic here.
            # I may move it to a seprate file, or keep it here forever
            response = r.get(self.url, stream=True, impersonate="chrome124")

            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))
            downloaded_size = 0

            with open(self.save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    if total_size:
                        percent = int(downloaded_size / total_size * 100)
                        self.signals.progress.emit(percent)
            response.close()
            self.signals.finished.emit()

        except Exception as e:
            logger.error(f"failed to download {self.url} {e}")
