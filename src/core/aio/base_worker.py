from PySide6.QtCore import QObject, QRunnable, Signal


class WorkerSignals(QObject):
    finished = Signal()
    progress = Signal(int)
    error = Signal(str)

class BaseWorker(QRunnable):
    def __init__(self):
        super().__init__()
        self.glob_signals = WorkerSignals()

    def run(self):
        # Implementation in subclasses
        pass
