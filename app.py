import os
import sys

from PySide6.QtWidgets import QApplication
from src.core import AppContainer
# import qss_reloader
from src.core.utils import resource_path, get_logger

logger = get_logger(__name__)

os.environ["QT_QPA_PLATFORM"] = "xcb"

def load_stylesheet(app: QApplication):
    style_path = resource_path("src/ui/styles/style.qss")

    full_qss = ""
    if os.path.exists(style_path):
        logger.info(f"Loading stylesheet: {style_path}")
        with open(style_path, "r") as f:
            full_qss = f.read()
    else:
        logger.warning(f"Stylesheet not found: {style_path}")

    app.setStyleSheet(full_qss)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    load_stylesheet(app)
    # reloader = qss_reloader.QSSReloader(app, qss_paths=[resource_path("src/ui/styles/style.qss")], debounce_ms=100)
    app_container = AppContainer()
    app_container._main_view.show()
    sys.exit(app.exec())
