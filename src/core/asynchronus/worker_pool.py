from PySide6.QtCore import QRunnable, QThreadPool

from ..tools import get_img_data


class WorkerPool:
    def __init__(self):
        self.WORKER_POOL = QThreadPool.globalInstance()
        self.WORKER_POOL.setMaxThreadCount(5)

    def run_in_thread_pool(self, worker):
        self.WORKER_POOL.start(worker)

class ThumbnailFetchWorker(QRunnable):
    def __init__(self, id, url, signals):
        super().__init__()
        self.signals = signals
        self.id = id
        self.url = url

    def run(self):
        img_data = get_img_data(self.url)
        self.signals.thumbnail_fetch_finished.emit(self.id, img_data)
