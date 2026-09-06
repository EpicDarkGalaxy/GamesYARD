from dataclasses import dataclass
from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtGui import QPixmap

from src.core.utils.log import get_logger
from src.ui.components.captcha_dialog import CaptchaBrowserDialog

logger = get_logger(__name__)

if TYPE_CHECKING:
    from src.core.app_coordinator import AppCoordinator


@dataclass
class DownloadViewState:
    id: str
    total_size: int = 0
    name: str = "NONAME"
    progress: int = 0
    speed: float = 0
    eta: int = 0
    downloaded_size: int = 0
    resume_supported: bool = False
    paused: bool = False
    is_downloading: bool = False
    has_finished: bool = False
    has_failed: bool = False
    banner: QPixmap | None = None


class DownloadViewModel(QObject):
    update_view = Signal(object)
    add_card = Signal(object)
    remove_card = Signal(str)  # Emitted when a download is canceled or finished
    open_captcha = Signal(str)

    def __init__(self):
        super().__init__()
        self._app_coordinator: AppCoordinator = None
        self._downloads: dict[str, DownloadViewState] = {}

    def initialize(self, coordinator):
        self._app_coordinator = coordinator
        self.bind_signals()

    def bind_signals(self):
        self._app_coordinator.download_manager.download_state_changed.connect(
            self._handle_download_state_changed
        )
        self._app_coordinator.download_manager.download_started.connect(self.add_download)
        self._app_coordinator.download_manager.download_cancelled.connect(self._handle_download_cancelled)
        self._app_coordinator.download_manager.captcha_required.connect(self.open_captcha.emit)

    def _update_download_model(self, download_view_state: DownloadViewState, download_state) -> None:
        download_view_state.downloaded_size = int(download_state.downloaded_size)
        download_view_state.progress = int(download_state.progress)
        download_view_state.total_size = int(download_state.total_size)
        download_view_state.speed = float(download_state.speed)
        download_view_state.eta = int(download_state.eta)
        download_view_state.is_downloading = bool(download_state.is_downloading)
        download_view_state.has_failed = bool(download_state.has_failed)
        download_view_state.has_finished = bool(download_state.has_finished)
        download_view_state.resume_supported = bool(download_state.resume_supported)
        download_view_state.paused = bool(download_state.paused)
        self.update_view.emit(download_view_state)

    @Slot(str, str)
    def add_download(self, download_id, downlaod_name=""):
        logger.debug(f"Adding downlaod: {download_id}")

        dl_model = self._downloads.get(download_id, None)
        if dl_model:
            self.add_card.emit(dl_model)
        else:
            logger.warning(f"Download Model was not found: {download_id}")

    @Slot(str, str, str, object)
    def requesting_download(
        self,
        url: str,
        download_id: str,
        download_name: str = "NONAME",
        banner: QPixmap | None = None,
    ):
        logger.debug(
            f"Starting download: id={download_id}, url={url}"
        )
        self._downloads[download_id] = DownloadViewState(id=str(download_id), name=download_name, banner=banner)
        self._app_coordinator.download_manager.add_download(
            url, download_id, download_name
        )

    def requesting_cancel_download(self, download_id: str):
        logger.debug(f"Cancelling download: id={download_id}")
        self._app_coordinator.download_manager.stop_download(download_id)

    def requesting_pause_download(self, download_id: str):
        logger.debug(f"Pausing download: id={download_id}")
        self._app_coordinator.download_manager.pause_download(download_id)

    def requesting_resume_download(self, download_id: str):
        logger.debug(f"Resuming download: id={download_id}")
        self._app_coordinator.download_manager.resume_download(download_id)

    @Slot(str)
    def _handle_download_cancelled(self, download_id: str):
        logger.debug(f"Download canceled: id={download_id}")
        _= self._downloads.pop(download_id, None)
        self.remove_card.emit(download_id)

    @Slot(object)
    def _handle_download_state_changed(self, download_state):
        logger.debug(f"Download state changed: id={download_state.id}, is_downloading={download_state.is_downloading}")

        if download_state.id not in self._downloads and download_state.is_downloading:  # Download resumed
            self.add_download(download_state.id, download_state.name)
        else:  # Download in progress or failed, finished and canceled
            download_model = self._downloads[download_state.id]
            self._update_download_model(download_model, download_state)
