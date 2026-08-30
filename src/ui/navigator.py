from PySide6.QtCore import QObject, Signal

from src.core.utils.log import get_logger

logger = get_logger(__name__)

class Navigator(QObject):
    request_page_change = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self._page_registry = {}

    def register_page(self, key: str, widget):
        logger.info(f"Registering page: {key}")
        self._page_registry[key] = widget

    def go_to(self, key: str):
        logger.info(f"Navigating to page: {key}")
        self.request_page_change.emit(key)
