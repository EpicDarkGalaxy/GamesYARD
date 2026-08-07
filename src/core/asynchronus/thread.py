from ..signals import IconWorkerSignals
from ..signals import FetchWorkerSignals
from ..utils import get_img_data
from ..log import get_logger
from PySide6.QtCore import (
    QThread, QThreadPool, QRunnable
)

logger = get_logger(__name__)

class Worker(QThread):
    def __init__(self):
        self.thread_pool = QThreadPool.globalInstance()
        self.thread_pool.setMaxThreadCount(5)

    def add_to_pool(self, worker: object):
        self.thread_pool.start(worker)

    def clear_thread_pool(self):
        self.thread_pool.clear()

class IconFetchWorker(QRunnable):
    def __init__(self, index: int = 0, img_url: str = ""):
        super.__init__()
        self.index = index
        self.img_url = img_url
        self.icon_fetched_signal = IconWorkerSignals.icon_fetched

    def run(self):
            logger.info(f"Icon Fetch Thread deployed")
            if self.img_url is not None:
                logger.info(f"Fetching icon from {self.img_url}")
                img_data = get_img_data(self.img_url)

                if img_data:
                    self.signals.icon_fetched.emit(self.item_index, img_data)
                else:
                    logger.warning(f"Could not fetched img_data, so will set a placeholder")

class FetchWorker(Worker):
    def __init__(self, search_query, game_fetcher):
        self.search_query = search_query
        self.game_fetcher = game_fetcher
        self.signals = FetchWorkerSignals()

        self.items = []

    def run(self):
        logger.info(f"Icon Fetch Thread deployed")
        self.items = self.game_fetcher.get_game_list(self.search_query)
        if (len(self.items) > 0):
            self.signals.fetch_finished.emit(self.items)
        else:
            self.signals.fetch_fail.emit() # Fire Fetch_Fail signal to reset some things 