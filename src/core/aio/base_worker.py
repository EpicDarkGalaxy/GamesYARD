from PySide6.QtCore import QObject, QRunnable, Signal
from .worker_signals import WorkerSignals


class BaseWorker(QRunnable):
    def __init__(self):
        super().__init__()
        self.signals = WorkerSignals()

    def run(self):
        # Implementation in subclasses
        pass
