from dataclasses import asdict, dataclass, field
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
    id: str
    name: str=""
    save_path: str = ""
    url: str = ""
    host_url: str = ""
    total_size: int = 0
    downloaded_size: int = 0
    progress: int = 0
    is_downloading: bool = False
    has_finished: bool = False
    has_failed: bool = False
    speed: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

class DownloadManager(QObject):
    download_started = Signal(str)
    download_finished = Signal(str)
    download_progress = Signal(str, int)
    download_failed = Signal(str)
    download_canceled = Signal(str)

    download_state_changed = Signal(Download)  # Download Model
    providers_found = Signal(dict)

    def __init__(self, task_runner: "TaskRunner"):
        super().__init__()
        self.download_queue: dict[str, Download] = {}
        self.is_downloading: bool = False
        self.task_runner = task_runner
        self.active_workers: dict[str, Any] = {}

    def add_download(self, save_path: str, provider_url: str, download_id: str, download_name: str="NONAME"):
        providers = ProviderFactory()
        provider = providers.get_provider(provider_url)
        if provider:
            download = Download(id=download_id, name=download_name, save_path=save_path, host_url=provider_url)
            self.download_queue[download_id] = download
            self.task_runner.run_task(provider.extract_dl_url, self._handle_dl_url, provider_url, return_value=download_id)
        else:
            raise Exception("Provider not found")

    def start_download(self, download_id: str):
        download = self.download_queue.get(download_id)
        if download and download.url:
            dl_worker = DownloadWorker(download.url, download.save_path, download.id)
            dl_worker.signals.download_progress.connect(self._handle_download_progress)
            dl_worker.signals.download_finished.connect(self._handle_download_finished)
            download.is_downloading = True

            self._handle_download_started(download_id)
            self.task_runner.run_worker(dl_worker)

    def stop_all_downloads(self):
        for download_id, worker in list(self.active_workers.items()):
            worker.stop()
        self.active_workers.clear()
        for download in self.download_queue.values():
            if download.is_downloading:
                download.is_downloading = False
                download.has_failed = True
                self.download_state_changed.emit(download)
                self.download_canceled.emit(download.id)
        self.task_runner.pool.clear()

    def get_providers(self, game_title: str):
        scraper = FourFNetScraper()
        self.task_runner.run_task(scraper.find_game_page, self._handle_game_page, game_title)

    def _handle_download_started(self, download_id: str):
        download = self.download_queue.get(download_id)
        if download:
            self.download_state_changed.emit(download)

    @Slot(str)
    def _handle_game_page(self, game_page: str):
        scraper = FourFNetScraper()
        self.task_runner.run_task(scraper.fetch_download_links, self._handle_providers, game_page)

    @Slot(dict)
    def _handle_providers(self, providers: dict):
        self.providers_found.emit(providers)

    @Slot(dict)
    def _handle_download_progress(self, download_progress: dict):
        download = self.download_queue.get(download_progress["download_id"])
        if download:
            download.progress = download_progress["percent"]
            download.total_size = download_progress["total_size"]
            download.downloaded_size = download_progress["downloaded_size"]
            download.speed = download_progress["speed"]
            self.download_state_changed.emit(download)

    @Slot(bool, str)
    def _handle_download_finished(self, result: bool, download_id: str):
        if result:
            self.download_finished.emit(download_id)
        else:
            self.download_failed.emit(download_id)

    @Slot(str, str)
    def _handle_dl_url(self, dl_url: str, download_id: str):
        download = self.download_queue.get(download_id)
        if dl_url and download:
            download.url = dl_url
            self.start_download(download_id)
