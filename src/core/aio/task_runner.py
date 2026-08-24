from PySide6.QtCore import QObject, QThreadPool


class TaskRunner(QObject):
    def __init__(self):
        super().__init__()
        self.pool = QThreadPool.globalInstance()
        self.pool.setMaxThreadCount(4)

    def run(self, worker):
        self.pool.start(worker)
