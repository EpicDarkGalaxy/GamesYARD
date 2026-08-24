from ...tools.utils import get_img_data
from ..base_worker import BaseWorker
from ..worker_signals import ThumbnailWorkerSignals


class ThumbnailFetchWorker(BaseWorker):
    def __init__(self, id, url):
        super().__init__()
        self.signals = ThumbnailWorkerSignals()
        self.id = id
        self.url = url

    def run(self):
        img_data = get_img_data(self.url)
        self.signals.thumbnail_fetch_finished.emit(self.id, img_data)
