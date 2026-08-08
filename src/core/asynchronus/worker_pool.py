from PySide6.QtCore import QRunnable, QThreadPool, QObject, Slot
from ..signals import IconWorkerSignals
from ..utils import get_img_data

worker_pool = QThreadPool()
worker_pool.setMaxThreadCount(5)

def run_in_thread_pool(worker, on_finish=None):

    if (on_finish): worker.signals.icon_fetched.connect(on_finish)

    def cleanup(self):
        worker.deleteLater()
        worker_pool.clear()

    worker.signals.finsihed.connect(cleanup)
    worker_pool.start(worker)

class IconFetchWorker(QRunnable):
    signals = IconWorkerSignals()

    def __init__(self, url: str):
        super().__init__()
        self.url = url

    @Slot()
    def run(self):
        img_data = get_img_data(self.url)
        if (img_data):
            self.signals.icon_fetched.emit(img_data)
            self.signals.finished.emit()
