from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any
from uuid import uuid1

from PySide6.QtCore import QObject, Signal, Slot

from src.core.services.scrapers.scraper_4fnet import FourFNetScraper

from ..aio.workers import DownloadWorker, Worker
from ..services.providers import ProviderFactory
from ..utils.log import get_logger

if TYPE_CHECKING:
    from ..aio import TaskRunner

logger = get_logger(__name__)

@dataclass
class Download:
    download_id: str
    save_path: str = ""
    download_url: str = ""
    host_url: str=""
    download_progress: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)

class DownloadManager(QObject):
    download_started = Signal(str)
    download_finished = Signal(str)
    download_progress = Signal(str ,int)
    download_failed = Signal(str)
    download_canceled = Signal(str)

    found_providers = Signal(dict)

    def __init__(self, task_runner: "TaskRunner"):
        super().__init__()
        self.download_queue: dict[str, Download] = {}
        self.is_downloading: bool= False
        self.task_runner = task_runner
        self.active_workers: dict[str, Any]= {}

    def store_download_metadata(self, download_id: str, metadata: dict[str, any]):
        download = self.download_queue.get(download_id)
        if download:
            download.metadata = metadata
            logger.info(f"Metadata stored for download: {download_id}")
        else:
            logger.warning(f"Could not store metadata: {download_id} not in queue")

    def get_download_metadata(self, host_url: str = "") -> dict[str, Any]:
        for download in self.download_queue.values():
            if download.host_url == host_url:
                logger.info(f"Metadata found for URL: {host_url}")
                return download.metadata
        logger.warning(f"No metadata found for URL: {host_url}")
        return {}

    def get_download_providers(self, game_title: str):
        logger.info(f"Searching for game: {game_title}")
        scraper = FourFNetScraper()
        self.task_runner.run_task(scraper.find_game_page, self._handle_game_page, game_title)

    def _handle_game_page(self, game_page: str):
        logger.info(f"Fetching download links for page: {game_page}")
        scraper = FourFNetScraper()
        self.task_runner.run_task(
            scraper.fetch_download_links,
            self._handle_found_providers,
            game_page)

    def _handle_found_providers(self, result: dict):
        self.found_providers.emit(result)

    def queue_download(self, save_path: str, provider_url: str, download_id: str):
        """
        Attempts to download a game from the given host URL.
        """
        provider = ProviderFactory.get_provider(url=provider_url)
        if not provider:
            logger.error(f"no provider found for {provider_url}, skipping download")
            return

        download = Download(save_path=save_path, download_id=download_id, host_url=provider_url)
        self._add_to_queue(download)
        self.task_runner.run_task(provider.extract_dl_url, self._handle_url_extracted, provider_url, return_value=download_id)

    @Slot(str, str)
    def _handle_url_extracted(self, download_url, download_id):
        download = self.download_queue[download_id]
        download.download_url = download_url
        self.start_download(download)

    def start_download(self, download: Download):
        logger.info(f"Starting download: [{download.download_id}] to [{download.save_path}]")

        download_worker = DownloadWorker(download.download_url, download.save_path, download.download_id)
        download_worker.signals.download_finished.connect(self._handle_download_success)
        download_worker.signals.download_fail.connect(self._handle_download_failure)
        download_worker.signals.download_progress.connect(self._handle_download_progress)
        self.task_runner.run_worker(download_worker)
        self.active_workers[download.download_id] = download_worker
        self.download_started.emit(download.download_id)

    def stop_download(self, download_id: str):
        """
        Stops a specific download by ID.

        Args:
            download_id (str): The unique identifier of the download to stop.
        """
        worker = self.active_workers.pop(download_id, None)
        if worker:
            worker.is_cancelled = True
            logger.info(f"Stopping worker for download: {download_id}")
            self.download_canceled.emit(download_id)
            self._remove_from_queue(download_id)

    def stop_all_downloads(self):
        """
        Stops all active downloads.
        """
        for dl_id, worker in self.active_workers.items():
            worker.is_cancelled = True
            logger.info(f"Stopping worker for download: {dl_id}")
            self.download_canceled.emit(dl_id)
        self.active_workers.clear()
        self.download_queue.clear()
        self.update_download_state()

    def pause_download(self, ):
        pass

    def resume_download(self, ):
        pass

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

    @Slot(str, int)
    def _handle_download_progress(self, download_id: str, progress: int):
        self.download_progress.emit(download_id, progress)

    @Slot(str)
    def _handle_download_failure(self, download_id: str):
        logger.info(f"Download Failed: [{download_id}]")
        self._remove_from_queue(download_id=download_id)
        self.download_failed.emit(download_id)

    @Slot(str)
    def _handle_download_success(self, download_id: str):
        logger.info(f"Download Completed: [{download_id}]")
        self._remove_from_queue(download_id=download_id)
        self.download_finished.emit(download_id)
