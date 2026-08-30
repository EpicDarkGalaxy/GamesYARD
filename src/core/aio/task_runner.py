from PySide6.QtCore import QObject, QRunnable, QThreadPool


class TaskRunner(QObject):
    def __init__(self):
        super().__init__()
        self.pool = QThreadPool.globalInstance()
        self.pool.setMaxThreadCount(4)

        self.thumb_pool = QThreadPool()
        self.thumb_pool.setMaxThreadCount(2)

        self.gallery_pool = QThreadPool()
        self.gallery_pool.setMaxThreadCount(2)

    def run(self, worker: QRunnable):
        self.pool.start(worker)
