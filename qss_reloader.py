from pathlib import Path
from PySide6.QtCore import QFileSystemWatcher, QObject, QTimer, Slot
from PySide6.QtWidgets import QApplication


class QSSReloader(QObject):
    """Watches one or more .qss files and automatically reapplies them to

    the QApplication when saved.
    """

    def __init__(
        self,
        app: QApplication,
        qss_paths: list[str | Path],
        debounce_ms: int = 100,
    ):
        super().__init__()
        self.app = app
        self.qss_paths = [Path(p).resolve() for p in qss_paths]
        self.watcher = QFileSystemWatcher(self)

        # Debounce timer to prevent rapid duplicate reloads on single save
        self._debounce_timer = QTimer(self)
        self._debounce_timer.setSingleShot(True)
        self._debounce_timer.setInterval(debounce_ms)
        self._debounce_timer.timeout.connect(self._apply_styles)

        # Set up watched files
        self._setup_watcher()
        self.watcher.fileChanged.connect(self._on_file_changed)

        # Initial style application on startup
        self._apply_styles()

    def _setup_watcher(self) -> None:
        for path in self.qss_paths:
            if not path.exists():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("/* Stylesheet */", encoding="utf-8")
            self.watcher.addPath(str(path))

    @Slot(str)
    def _on_file_changed(self, file_path: str) -> None:
        path = Path(file_path)

        # Handle atomic saves: IDEs often delete and recreate the file,
        # which removes it from QFileSystemWatcher's internal tracking list.
        if str(path) not in self.watcher.files() and path.exists():
            self.watcher.addPath(str(path))

        # Restart debounce window
        self._debounce_timer.start()

    def _apply_styles(self) -> None:
        combined_qss = []
        for path in self.qss_paths:
            if path.is_file():
                try:
                    combined_qss.append(path.read_text(encoding="utf-8"))
                except Exception as e:
                    print(f"[QSS Reloader] Error reading {path.name}: {e}")

        self.app.setStyleSheet("\n".join(combined_qss))
        print("[QSS Reloader] Stylesheet updated.")
