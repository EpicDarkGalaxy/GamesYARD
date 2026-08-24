from ...tools.log import get_logger
from ..base_worker import BaseWorker
from ..worker_signals import UrlExtractorWorkerSignals

logger = get_logger(__name__)

class LinkExtractionWorker(BaseWorker):
    def __init__(self, method, url: str, id: str=""):
        super().__init__()
        self.url = url
        self.signals = UrlExtractorWorkerSignals()
        self.method = method # Extraction Logic Function
        self.id = id

    def run(self):
        try:
            result = self.method(self.url)
            # print(f"Extracted Link: {result}")
            self.signals.link_extracted.emit(result, self.id)
        except Exception as e:
            logger.error(f"failed to extract links from {self.url} {e}")
