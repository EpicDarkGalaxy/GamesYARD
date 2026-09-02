import os
import sys

from PySide6.QtWidgets import QApplication
from src.core import AppContainer
import qss_reloader

os.environ["QT_QPA_PLATFORM"] = "xcb"

def load_stylesheet(app: QApplication):
    style_dir = os.path.join(os.path.dirname(__file__), "src", "ui", "styles")

    # Define files in the order of priority
    files = ["variables.qss", "layouts.qss", "components.qss", "style.qss"]

    full_qss = ""
    for filename in files:
        path = os.path.join(style_dir, filename)
        if os.path.exists(path):
            with open(path, "r") as f:
                full_qss += f.read() + "\n"
        else:
            print(f"Warning: Stylesheet part not found: {path}")

    app.setStyleSheet(full_qss)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    style_dir = os.path.join(os.path.dirname(__file__), "src", "ui", "styles")
    qss_paths = [os.path.join(style_dir, f) for f in ["variables.qss", "layouts.qss", "components.qss", "style.qss"]]
    reloader = qss_reloader.QSSReloader(app, qss_paths=["src/ui/styles/style.qss"], debounce_ms=100)
    app_container = AppContainer()
    app_container._main_view.show()
    sys.exit(app.exec())
