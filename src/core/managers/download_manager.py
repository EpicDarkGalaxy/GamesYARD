from dataclasses import asdict, dataclass, field
from typing import TYPE_CHECKING, Any
from uuid import uuid1
import os
from PySide6.QtCore import QObject, Signal, Slot

from src.core.services.scrapers import *

from ..aio.workers import DownloadWorker, Worker
from ..services.providers import ProviderFactory
from src.core.utils import get_logger, get_filename_for_url, get_default_download_dir

if TYPE_CHECKING:
    from ..aio import TaskRunner

logger = get_logger(__name__)


@dataclass
class DownloadState:
    id: str
    name: str=""
    save_path: str = ""
    url: str = ""
    host_url: str = ""
    total_size: int = 0
    downloaded_size: int = 0
    progress: int = 0
    paused: bool = False
    resume_supported: bool = False
    is_downloading: bool = False
    has_finished: bool = False
    has_failed: bool = False
    speed: float = 0.0
    eta: int = 0
    headers: dict = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

class DownloadManager(QObject):
    download_started = Signal(str, str)
    download_cancelled = Signal(str)
    download_state_changed = Signal(DownloadState)  # Download Model

    captcha_required = Signal(str)
    providers_found = Signal(dict)

    def __init__(self, task_runner: "TaskRunner"):
        super().__init__()
        self._task_runner = task_runner
        self._active_workers: dict[str, Any] = {}
        self._download_queue: dict[str, DownloadState] = {}
        self.is_downloading: bool = False # Flag to track if the download manager is currently downloading

    def add_download(self, provider_url: str, download_id: str, download_name: str="NONAME"):
        providers = ProviderFactory()
        provider = providers.get_provider(provider_url)
        if provider:
            download = DownloadState(id=download_id, name=download_name, host_url=provider_url)
            self._download_queue[download_id] = download
            self._task_runner.run_task(provider.extract_dl_url, self._handle_dl_url, provider_url, return_value=download_id)
        else:
            raise Exception(f"Provider not found: {provider_url}")

    def start_download(self, download_id: str):
        download = self._download_queue.get(download_id, None)
        if download and download.url:
            dl_worker = DownloadWorker(download.url, download.save_path, download.id, download.headers)
            dl_worker.signals.download_progress.connect(self._handle_download_progress)
            dl_worker.signals.download_finished.connect(self._handle_download_finished)
            download.is_downloading = True

            self._active_workers[download_id] = dl_worker
            self.download_started.emit(download_id, download.name)
            self._task_runner.run_worker(dl_worker)

    def stop_download(self, download_id: str):
        download = self._download_queue.pop(download_id, None)
        if download:
            logger.debug(f"Stopping download: id={download_id}")
            download.is_downloading = False
            download.has_failed = True
            self._remove_file(download.save_path)
            self.download_cancelled.emit(download.id)
            dl_worker = self._active_workers.pop(download_id, None)
            if dl_worker:
                dl_worker.cancel()
        else:
            logger.warning(f"Download not found: id={download_id}")

    def _remove_file(self, save_path: str):
        if os.path.exists(save_path):
            os.remove(save_path)

    def stop_all_downloads(self):
        for download_id in list(self._download_queue):
            self.stop_download(download_id)
        self._download_queue.clear()
        self._active_workers.clear()
        self._task_runner.pool.clear()
        self.is_downloading = False

    def pause_download(self, download_id: str):
        worker = self._active_workers.pop(download_id, None)
        if worker:
            worker.pause()

    def resume_download(self, download_id: str):
        self.start_download(download_id)

    def get_providers(self, game_title: str):
        scrapers = [FourFNetScraper(), GameBountyScraper()]
        self._provider_aggregate: dict[str, dict[str, str]] = {}
        self._pending_scraper_count = len(scrapers)

        for scraper in scrapers:
            self._task_runner.run_task(
                scraper.find_game_url,
                self._handle_game_page,
                game_title,
                return_value=scraper,
            )

    @Slot(object, object)
    def _handle_game_page(self, game_url: str | None, scraper):
        if not game_url:
            self._on_scraper_done()
            return
        self._task_runner.run_task(
            scraper.scrape_download_urls,
            self._handle_providers,
            game_url,
        )

    @Slot(dict)
    def _handle_providers(self, providers: dict):
        self._provider_aggregate.update(providers)
        self._on_scraper_done()

    def _on_scraper_done(self):
        self._pending_scraper_count -= 1
        if self._pending_scraper_count <= 0:
            self.providers_found.emit(self._provider_aggregate)

    @Slot(dict)
    def _handle_download_progress(self, download_progress: dict):
        download = self._download_queue.get(download_progress["download_id"])
        if download:
            download.progress = download_progress["percent"]
            download.total_size = download_progress["total_size"]
            download.downloaded_size = download_progress["downloaded_size"]
            download.paused = download_progress["paused"]
            download.is_downloading = download_progress["is_downloading"]
            download.resume_supported = download_progress["resume_supported"]
            download.speed = download_progress["speed"]
            download.eta = download_progress["eta"]
            self.download_state_changed.emit(download)

    @Slot(bool, str)
    def _handle_download_finished(self, result: bool, download_id: str):
        download = self._download_queue.get(download_id)
        if not download:
            return
        download.is_downloading = False
        download.has_finished = result
        download.has_failed = not result
        self.download_state_changed.emit(download)

    @Slot(tuple, str)
    def _handle_dl_url(self, resolved: tuple[Any, ...], download_id: str):
        logger.debug(f"Handling dl_url: {resolved} for download_id: {download_id}")

        download = self._download_queue.get(download_id)
        if not download:
            return

        def _handle_failure():
            logger.error(f"Failed to resolve dl_url for download_id: {download_id}, resolved: {resolved}")
            download.has_failed = True
            self.download_state_changed.emit(download)
            self._download_queue.pop(download_id, None)

        if resolved and len(resolved) == 2:
            if isinstance(resolved[0], str) and resolved[0].startswith("CAPTCHA_REQUIRED"):
                self.captcha_required.emit(resolved[1].get("url"))
                return

            direct_url, metadata = resolved
            if direct_url and isinstance(metadata, dict):
                filename = metadata.get("filename")
                save_path = get_default_download_dir()
                headers = metadata.get("headers", {})

                if not filename:
                    filename = get_filename_for_url(direct_url, headers)

                download.save_path = os.path.join(save_path, filename)
                download.url = direct_url
                download.headers = headers
                self.start_download(download_id)
                return

        _handle_failure()
