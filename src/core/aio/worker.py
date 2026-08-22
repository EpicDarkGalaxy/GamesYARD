import os
from curl_cffi import requests as r

from PySide6.QtCore import QObject, QThread, Slot
from .worker_signals import (
    DownloadWorkerSignals,
    FetchWorkerSignals,
    LinkExtractorWorkerSignals
)
from ..tools import GameFetcher, get_logger

logger = get_logger(__name__)

class WorkerManager:
    threads = []
    workers = []

    def run_in_thread(self, worker, on_finish=None, on_fail=None, on_progress=None):
        thread = QThread()
        worker.moveToThread(thread)

        self.threads.append(thread)
        self.workers.append(worker)

        thread.started.connect(worker.run)

        if (on_fail): worker.signals.fail.connect(on_fail)
        if (on_finish): worker.signals.finished.connect(on_finish)
        if (on_progress): worker.signals.progress.connect(on_progress)

        worker.signals.finished.connect(self.cleanup)
        worker.signals.fail.connect(self.cleanup)

        thread.start()
        return thread, worker

    def cleanup(self):
        for thread, worker in zip(self.threads, self.workers):
            thread.quit()
            thread.wait()
            worker.deleteLater()
        self.threads.clear()
        self.workers.clear()

class GameFetchWorker(QObject):
    def __init__ (self, search_query: str, game_fetcher: GameFetcher, load_more:bool=False):
        super().__init__()
        self.search_query = search_query
        self.game_fetcher = game_fetcher
        self.signals = FetchWorkerSignals()
        self.load_more = load_more

    @Slot()
    def run(self):
        cards_list = self.game_fetcher.get_game_list(self.search_query, self.load_more)
        self.signals.fetch_finished.emit(cards_list)
        self.signals.finished.emit()

class DownloadWorker(QObject):
    def __init__(self, url: str, save_path: str, download_id: str=""):
        super().__init__()
        self.url = url
        self.save_path = save_path
        self.download_id = download_id
        self.signals = DownloadWorkerSignals()
        self.is_cancelled = False

    def cancle(self):
        self.is_cancelled = True

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
                    if (self.is_cancelled):
                        response.close()
                        f.close()
                        if (os.path.exists(self.save_path)):
                            os.remove(self.save_path)
                        self.signals.cancelled.emit()
                        self.signals.finished.emit()
                        logger.info(f"Download Cancelled: {self.url}")
                        return
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    if total_size:
                        percent = int(downloaded_size / total_size * 100)
                        self.signals.progress.emit(percent)
            response.close()
            self.signals.download_finished.emit(self.download_id)
            self.signals.finished.emit()

        except Exception as e:
            logger.error(f"failed to download {self.url} {e}")

class LinkExtractionWorker(QObject):
    def __init__(self, method, url: str, id: str=""):
        super().__init__()
        self.url = url
        self.signals = LinkExtractorWorkerSignals()
        self.method = method # Extraction Logic Function
        self.id = id

    def run(self):
        try:
            result = self.method(self.url)
            print(f"Extracted Link: {result}")
            self.signals.link_extracted.emit(result, self.id)
        except Exception as e:
            logger.error(f"failed to extract links from {self.url} {e}")
