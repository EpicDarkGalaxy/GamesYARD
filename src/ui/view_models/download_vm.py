from dataclasses import dataclass
from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtGui import QPixmap

from src.core.utils.log import get_logger

logger = get_logger(__name__)

if TYPE_CHECKING:
    from src.core.app_coordinator import AppCoordinator


@dataclass
class DownloadModel:
    total_size: int
    name: str = "NONAME"
    id: str = "NOID"
    progress: int = 0
    speed: float = 0
    downloaded_size: int = 0
    is_downloading: bool = False
    has_finished: bool = False
    has_failed: bool = False
    banner: QPixmap | None = None


class DownloadViewModel(QObject):
    update_view = Signal(object)
    add_card = Signal(object)
    remove_card = Signal(str)  # Emitted when a download is canceled or finished

    def __init__(self):
        super().__init__()
        self._app_coordinator: AppCoordinator = None
        self._downloads: dict[str, DownloadModel] = {}
        self._banners: dict[str, QPixmap] = {}

    def initialize(self, coordinator):
        self._app_coordinator = coordinator
        self.bind_signals()

    def bind_signals(self):
        self._app_coordinator.download_manager.download_state_changed.connect(
            self._handle_download_state_changed
        )

    def _update_download_model(self, download_model: DownloadModel, download) -> None:
        download_model.downloaded_size = int(download.downloaded_size)
        download_model.progress = int(download.progress)
        download_model.speed = float(download.speed)
        download_model.is_downloading = bool(download.is_downloading)
        download_model.has_failed = bool(download.has_failed)
        download_model.has_finished = bool(download.has_finished)

    def add_download(self, download):
        logger.debug(f"Adding download: {download}")
        download_id = str(download.id)
        download_model = DownloadModel(
            id=download_id,
            name=download.name,
            total_size=download.total_size,
            banner=self._banners.get(download_id, None),
        )

        self._update_download_model(download_model, download)
        self._downloads[download_id] = download_model
        self.add_card.emit(download_model)

    @Slot(str, str, str, str, object)
    def download(
        self,
        save_path: str,
        url: str,
        download_id: str,
        download_name: str = "NONAME",
        banner: QPixmap | None = None,
    ):
        logger.debug(
            f"Starting download: id={download_id}, url={url}, save_path={save_path}"
        )
        if banner:
            self._banners[download_id] = banner
        self._app_coordinator.download_manager.add_download(
            save_path, url, download_id, download_name
        )

    def cancel_download(self, download_id: str):
        logger.debug(f"Cancelling download: id={download_id}")
        self._app_coordinator.download_manager.stop_download(download_id)

    def pause_download(self, download_id: str):
        pass

    @Slot(object)
    def _handle_download_state_changed(self, download):
        if download.id not in self._downloads and download.is_downloading:
            self.add_download(download)
        elif download.id in self._downloads and not download.is_downloading:
            self.remove_card.emit(download.id)
        else:
            download_model = self._downloads[download.id]
            self._update_download_model(download_model, download)
            self.update_view.emit(download_model)
