from ..base_worker import BaseWorker
from ..worker_signals import WorkerSignals
from src.core.utils.log import get_logger

logger = get_logger(__name__)

class Worker(BaseWorker):
    def __init__(self, method, *args, context=None, **kwargs):
        super().__init__()
        self.method = method
        self.args = args
        self.kwargs = kwargs
        self.context = context
        logger.debug(f"Worker initialized with method: {self.method.__name__}, args: {self.args}, kwargs: {self.kwargs}, context: {self.context}")
    def run(self):
        try:
            result = self.method(*self.args, **self.kwargs)
            self.signals.result_ready.emit(result, self.context)
        except Exception as e:
            logger.error(f"UniversalWorker Error: {e}")
