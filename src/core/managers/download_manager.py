from PySide6.QtCore import QObject, Signal, Slot

from typing import TYPE_CHECKING
from ..aio import DownloadWorker, LinkExtractionWorker
from ..downloaders import DownloaderFactory
from ..tools.log import get_logger

if TYPE_CHECKING:
    from ..aio import WorkerManager

logger = get_logger(__name__)


class Download:
    def __init__(self, save_path="", download_url="", download_id="", manager=None):
        self.save_path = save_path
        self.download_url = download_url
        self.download_id = download_id
        self.download_progress = 0
        self._manager = manager

    def update_progress(self, progress):
        logger.info(f"Download progress: {progress}")
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

    def attempt_download(self, save_path: str, provider_url: str, download_id: str):
        """
        Attempts to download a game from the given host URL.
        """
        provider = DownloaderFactory.get_provider(url=provider_url)
        if not provider:
            logger.error(f"no provider found for {provider_url}, skipping download")
            return

        download = Download(save_path=save_path, download_id=download_id, manager=self)
        self.update_download_queue(download_id, download, True)

        self.link_worker = LinkExtractionWorker(provider.get_method(), provider_url, download_id)
        self.link_worker.signals.link_extracted.connect(self.download_url_found)
        self.worker_manager.run_in_thread(self.link_worker)

    @Slot(str, str)
    def download_url_found(self, download_url, download_id):
        logger.info(f"Link extracted: {download_url}")

        download = self.download_queue[download_id]
        download.download_url = download_url
        self.start_download(download)


    def start_download(self, download: Download):
        logger.info(f"Starting download: [{download.download_url}] to [{download.save_path}]")

        self.download_worker = DownloadWorker(download.download_url, download.save_path, download.download_id)
        self.download_worker.signals.download_finished.connect(self.update_download_queue)
        self.download_worker.signals.download_fail.connect(self.on_download_fail)
        self.worker_manager.run_in_thread(self.download_worker, on_progress=download.update_progress)

    def stop_download(self, ):
        # Later, we will use a list containing the deployed workers
        if (hasattr(self, 'download_worker') and self.download_worker):
            self.download_worker.is_cancelled = True
            self.download_worker = None

    def update_download_state(self):
        if (self.download_queue):
            logger.info("There is a Download RUNNING.")
            self.is_downloading = True
        else:
            logger.info("All Downloads FINISHED.")
            self.is_downloading = False

    @Slot(str, object, bool)
    def update_download_queue(self, download_id: str="", download=None, adding: bool=False):
        logger.debug(f"update_download_queue: download_id=[{download_id}], download=[{download}], adding=[{adding}]")

        if (adding and download):
            logger.info(f"Adding download to queue with id: [{download_id}]")
            self.download_queue[download_id] = download
        elif (self.download_queue.get(download_id)):
            logger.warning(f"Download Removed: [{download_id}]")
            self.download_queue.pop(download_id)
        else:
            logger.warning("Could not Update Download queue")

        self.update_download_state()

    @Slot(str)
    def on_download_fail(self, download_id: str):
        logger.info(f"Download Failed: [{download_id}]")
        self.update_download_queue(download_id=download_id) # Remove download from queue
        self.download_failed.emit(download_id)

    def on_download_finish(self, download_id: str):
        logger.info(f"Download Completed: [{download_id}]")
        self.download_finished.emit(download_id)

    def pause_download(self, ):
        pass

    def resume_download(self, ):
        pass
