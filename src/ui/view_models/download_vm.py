from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, Signal, Slot

from src.core.utils.log import get_logger

logger = get_logger(__name__)

if TYPE_CHECKING:
    from src.core.app_coordinator import AppCoordinator

@dataclass
class DownloadModel:
    id: str
    name: str
    total_size: int
    downloaded_size: int
    progress: int
    speed: float = 0
    is_downloading: bool = False
    has_finished: bool = False
    has_failed: bool = False

class DownloadViewModel(QObject):
    update_view = Signal(object)
    add_card = Signal(str, str)

    def __init__(self):
        super().__init__()
        self._app_coordinator: AppCoordinator = None
        self._downloads: dict[str, DownloadModel] = {}

    def initialize(self, coordinator):
        self._app_coordinator = coordinator
        self.bind_signals()

    def bind_signals(self):
        self._app_coordinator.download_manager.download_state_changed.connect(self._handle_download_state_changed)

    def _update_download_model(self, download_model: DownloadModel, download) -> None:
        download_model.name = str(download.name)
        download_model.total_size = int(download.total_size)
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
            name="",
            total_size=0,
            downloaded_size=0,
            progress=0,
        )
        self._update_download_model(download_model, download)
        self._downloads[download_id] = download_model
        self.add_card.emit(download_id, download.name)

    def download(self, save_path: str, url: str, download_id: str, download_name: str="NONAME"):
        logger.debug(f"Starting download: id={download_id}, url={url}, save_path={save_path}")
        self._app_coordinator.download_manager.add_download(save_path, url, download_id, download_name)

    def cancel(self):
        pass

    @Slot(object)
    def _handle_download_state_changed(self, download):
        if download.id not in self._downloads:
            self.add_download(download)
        else:
            download_model = self._downloads[download.id]
            self._update_download_model(download_model, download)
            self.update_view.emit(download_model)
