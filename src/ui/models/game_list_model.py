from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt, Slot
from PySide6.QtGui import QPixmap
from src.core.utils.log import get_logger

logger = get_logger(__name__)


class GameListModel(QAbstractListModel):
    def __init__(self, games=None, coordinator=None):
        super().__init__()
        self.coordinator = coordinator
        self._games = games or []
        self.thumbnails: dict[int, dict[str, QPixmap]] = {}

    def rowCount(self, parent=QModelIndex()):
        return len(self._games)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            return self._games[index.row()]
        return None

    def update_data(self, games):
        self.beginResetModel()
        self._games = games
        self.endResetModel()

    def fetch_thumbnail(self, row, game_id, url):
        if row in self.thumbnails and game_id in self.thumbnails[row]:
            # logger.debug(f"Thumbnail for row {row} already exists, skipping fetch.")
            return

        if self.coordinator:
            logger.info(f"Fetching thumbnail for row {row}, game_id {game_id}")
            self.thumbnails[row] = {game_id: QPixmap()}  # Avoid duplicate worker initiation

            self.coordinator.task_runner.run_task(
                self.coordinator.asset_manager.get_thumbnail,
                self._handle_thumbnail,
                game_id,
                url,
                return_value=(row, game_id)
            )
        else:
            logger.warning(f"Coordinator is empty or a different type!")

    @Slot(bytes, tuple)
    def _handle_thumbnail(self, img_data: bytes, identity):
        if img_data:
            pix = QPixmap()
            if pix.loadFromData(img_data):
                pix = pix.scaled(
                    320,
                    180,
                    Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                    Qt.TransformationMode.SmoothTransformation,
                )
                self.thumbnails[identity[0]] = {identity[1]: pix}
                self.dataChanged.emit(self.index(identity[0], 0), self.index(identity[0], 0))
            else:
                logger.error(f"Failed to load thumbnail data for row {identity[0]}")
        else:
            logger.warning(f"Received empty thumbnail data for row {identity[0]}")

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.viewport().update()  # Force repaint to clear hover effect when leaving the view

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.viewport().update()  # Force repaint to update hover effect as mouse moves
