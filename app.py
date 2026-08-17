import os
import sys

from PySide6.QtWidgets import QApplication

from src.ui.windows import MainWindow
from src.core.manager import MANAGER


def load_stylesheet(app: QApplication):
    # Construct path to style.qss
    style_path = os.path.join(os.path.dirname(__file__), "src", "ui", "style.qss")

    if os.path.exists(style_path):
        with open(style_path, "r") as f:
            app.setStyleSheet(f.read())
    else:
        print(f"Warning: Stylesheet not found at {style_path}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    load_stylesheet(app)
    window = MainWindow()
    MANAGER.store_main_window(window)
    window.show()
    sys.exit(app.exec())
