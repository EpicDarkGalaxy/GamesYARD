from PySide6.QtCore import QRunnable, QThreadPool, Slot

from ..utils import get_img_data


class WorkerPool:
    def __init__(self) -> None:
        self.WORKER_POOL = QThreadPool.globalInstance()
        self.WORKER_POOL.setMaxThreadCount(5)

    def run_in_thread_pool(self, worker):
        self.WORKER_POOL.start(worker)

class ThumbnailFetchWorker(QRunnable):
    def __init__(self, data_card, signals):
        super().__init__()
        self.url = data_card.posterLink
        self.data_card = data_card
        self.signals = signals

    def run(self):
        img_data = get_img_data(self.url)
        if (img_data):
            self.signals.thumbnail_fetch_finished.emit(self.data_card, img_data)
        else:
            self.signals.thumbnail_fetch_finished.emit(None, None)
