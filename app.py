import os
import sys

from PySide6.QtWidgets import QApplication
from src.core.app_container import AppContainer

os.environ["QT_QPA_PLATFORM"] = "xcb"

def load_stylesheet(app: QApplication):
    # Construct path to style.qss
    style_path = os.path.join(os.path.dirname(__file__), "src", "ui", "styles", "style.qss")

    if os.path.exists(style_path):
        with open(style_path, "r") as f:
            app.setStyleSheet(f.read())
    else:
        print(f"Warning: Stylesheet not found at {style_path}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    load_stylesheet(app)
    app_container = AppContainer()
    app_container._main_view.show()
    sys.exit(app.exec())
