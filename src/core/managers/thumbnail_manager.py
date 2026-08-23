from PySide6.QtCore import QObject, Signal, Slot
from typing import TYPE_CHECKING
from ..tools.log import get_logger
from ..aio.worker_pool import ThumbnailFetchWorker

if TYPE_CHECKING:
    from ..aio.worker_pool import WorkerPool

logger = get_logger(__name__)

class ThumbnailManager(QObject):
    thumbnail_ready = Signal(str, bytes)

    def __init__(self, worker_pool: "WorkerPool"):
        super().__init__()
        self.worker_pool = worker_pool

    def request_thumbnail(self, id: str, img_url: str):
        logger.info(f"Starting Worker for thumbnail for url {img_url}")

        thumbnail_worker = ThumbnailFetchWorker(id, img_url)
        thumbnail_worker.signals.thumbnail_fetch_finished.connect(self.thumb_fetched)
        self.worker_pool.run_in_thread_pool(thumbnail_worker)

    @Slot(str, bytes)
    def thumb_fetched(self, id: str, img_data: bytes):
        logger.info(f"Thumbnail Worker finished for card {id}")
        self.thumbnail_ready.emit(id, img_data)
