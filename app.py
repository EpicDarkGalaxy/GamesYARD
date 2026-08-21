import os
import sys

from PySide6.QtWidgets import QApplication

from src.ui.window_controller import WindowController
from src.core.manager import Manager
from src.ui.presenters import MainPresenter
from src.ui.windows.main_window import MainWindow


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
    manager = Manager()
    controller = WindowController(manager)
    controller.show_MainWindow()
    sys.exit(app.exec())
