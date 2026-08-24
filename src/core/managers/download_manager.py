from PySide6.QtCore import QObject, Signal, Slot

from typing import TYPE_CHECKING
from ..aio import DownloadWorker, LinkExtractionWorker
from ..downloaders import DownloaderFactory
from ..tools.log import get_logger
from dataclasses import dataclass, field
from typing import Any, Optional

if TYPE_CHECKING:
    from ..aio import WorkerManager

logger = get_logger(__name__)

@dataclass
class Download:
    download_id: str
    save_path: str = ""
    download_url: str = ""
    download_progress: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)
    _manager: Optional["DownloadManager"] = None

    def update_progress(self, progress: int) -> None:
        self.download_progress = progress
        if self._manager:
            self._manager.download_progress.emit(self.download_progress)

class DownloadManager(QObject):
    download_started = Signal(str)
    download_finished = Signal(str)
    download_progress = Signal(int)
    download_failed = Signal(str)
    download_cancelled = Signal()

    def __init__(self, worker_manager: "WorkerManager"):
        super().__init__()
        self.download_queue: dict[str, Download] = {}
        self.is_downloading = False
        self.worker_manager = worker_manager

    def store_download_metadata(self, download_id: str, metadata: dict[str, any]):
        download = self.download_queue.get(download_id)
        if download:
            setattr(download, 'metadata', metadata)
            logger.info(f"Metadata stored for download: {download_id}")
        else:
            logger.warning(f"Could not store metadata: {download_id} not in queue")

    def queue_download(self, save_path: str, provider_url: str, download_id: str):
        """
        Attempts to download a game from the given host URL.
        """
        provider = DownloaderFactory.get_provider(url=provider_url)
        if not provider:
            logger.error(f"no provider found for {provider_url}, skipping download")
            return

        download = Download(save_path=save_path, download_id=download_id, manager=self)
        self._add_to_queue(download)

        link_worker = LinkExtractionWorker(provider.get_method(), provider_url, download_id)
        link_worker.signals.link_extracted.connect(self.handle_url_extracted)
        self.worker_manager.run_in_thread(link_worker)

    @Slot(str, str)
    def handle_url_extracted(self, download_url, download_id):
        logger.info(f"URL extracted: {download_url}")
        download = self.download_queue[download_id]
        download.download_url = download_url
        self.start_download(download)

    def start_download(self, download: Download):
        logger.info(f"Starting download: [{download.download_url}] to [{download.save_path}]")

        self.download_worker = DownloadWorker(download.download_url, download.save_path, download.download_id)
        self.download_worker.signals.download_finished.connect(self.handle_download_success)
        self.download_worker.signals.download_fail.connect(self.handle_download_failure)
        self.worker_manager.run_in_thread(self.download_worker, on_progress=download.update_progress)

    def stop_download(self, download_id: str=""):
        # Later, we will use a list containing the deployed workers
        if (hasattr(self, 'download_worker') and self.download_worker):
            self.download_worker.is_cancelled = True
            self.download_worker = None
        self._remove_from_queue(download_id)

    def update_download_state(self):
        if (self.download_queue):
            logger.info("There is a Download RUNNING.")
            self.is_downloading = True
        else:
            logger.info("All Downloads FINISHED.")
            self.is_downloading = False

    def _add_to_queue(self, download: Download):
       logger.info(f"Adding download to queue: {download.download_id}")
       self.download_queue[download.download_id] = download
       self.update_download_state()

    def _remove_from_queue(self, download_id: str):
        logger.info("Removing download from queue")
        download = self.download_queue.pop(download_id, None)
        if not download:
            logger.warning(f"Download was not in queue: [{download_id}]")
        self.update_download_state()

    @Slot(str)
    def handle_download_failure(self, download_id: str):
        logger.info(f"Download Failed: [{download_id}]")
        self._remove_from_queue(download_id=download_id)
        self.download_failed.emit(download_id)

    @Slot(str)
    def handle_download_success(self, download_id: str):
        logger.info(f"Download Completed: [{download_id}]")
        self._remove_from_queue(download_id=download_id)
        self.download_finished.emit(download_id)

    def pause_download(self, ):
        pass

    def resume_download(self, ):
        pass
