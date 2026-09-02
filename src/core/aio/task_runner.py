from PySide6.QtCore import QObject, QRunnable, QThreadPool

from src.core.utils.log import get_logger

from .workers import Worker

logger = get_logger(__name__)

class TaskRunner(QObject):
    def __init__(self):
        super().__init__()
        self.pool = QThreadPool.globalInstance()
        self.pool.setMaxThreadCount(4)

    def run_task(self, func, callback, *args, return_value = None, **kwargs):
        logger.info(
            f"Running task: {func.__name__} with callback: {callback.__name__ if hasattr(callback, '__name__') else str(callback)}, "
            f"args: {args}, kwargs: {kwargs}, return_value: {return_value}"
        )
        worker = Worker(func, *args, context=return_value, **kwargs)
        _ = worker.signals.result_ready.connect(callback)
        self.pool.start(worker)

    def run_worker(self, worker: QRunnable):
        self.pool.start(worker)
