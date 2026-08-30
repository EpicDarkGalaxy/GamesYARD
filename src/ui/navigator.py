from PySide6.QtCore import QObject, Signal
<<<<<<< HEAD

from src.core.utils.log import get_logger
=======
from ..core.utils import get_logger
>>>>>>> 49411a3e9ffa7ace8a740fca7c33696c699c18bc

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
