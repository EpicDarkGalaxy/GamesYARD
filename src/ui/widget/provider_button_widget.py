from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QHBoxLayout, QProgressBar, QPushButton, QWidget
from uuid import uuid4


class ProviderButton(QWidget):
    download_requested = Signal(str, QWidget) # URL, Widget reference
    cancel_requested = Signal(str, QWidget) # self

    _is_downloading = False
    _is_downloaded = False

    def __init__(self, provider_name: str, landing_page_url: str="", on_click=None, on_cancel=None):
        super().__init__()
        self._id = str(uuid4())
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.provider_name = provider_name
        self.landing_page_url = landing_page_url

        self.btn = QPushButton(provider_name)
        self.btn.setObjectName("provider-btn")
        self.btn.clicked.connect(self.handle_click)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setVisible(False) # Hide by default!

        # Put them side-by-side or let progress_bar replace the button space
        self.main_layout.addWidget(self.btn)
        self.main_layout.addWidget(self.progress_bar)

        if (on_click):
            self.download_requested.connect(on_click)
        if (on_cancel):
            self.cancel_requested.connect(on_cancel)

    def handle_click(self):
        if (self._is_downloading):
            print(f"Requesting cancellation: {self.landing_page_url}")
            self.set_downloading_state(False)
            self.cancel_requested.emit(self.landing_page_url, self)
        else:
            print(f"Requesting download: {self.landing_page_url}")
            self.set_downloading_state(True)
            self.download_requested.emit(self.landing_page_url, self)

    def update_progress(self, value: int):
        self.progress_bar.setValue(value)

    def set_downloading_state(self, is_downloading: bool=False, is_downloaded: bool=False):
        self._is_downloading = is_downloading
        self._is_downloaded = is_downloaded

        if (is_downloaded):
            self.btn.setVisible(True)
            self.btn.setStyleSheet("""
                QPushButton {
                    background-color: green;
                }
                """)
            self.btn.setText("Donwload completed, click to redownload")
            self.progress_bar.setVisible(False)
            return

        if (is_downloading):
            self.btn.setVisible(False)
            self.btn.setText("Click to Cancel")
            self.progress_bar.setVisible(True)
        else:
            self.btn.setVisible(True)
            self.btn.setStyleSheet("")
            self.btn.setText(self.provider_name)
            self.progress_bar.setVisible(False)

    def enterEvent(self, event):
        if (self._is_downloading and not self._is_downloaded):
            self.btn.setStyleSheet("""
                QPushButton {
                    background-color: red;
                }
                """)
            self.btn.setVisible(True)
            self.progress_bar.setVisible(False)
            super().enterEvent(event)

    def leaveEvent(self, event):
        if (self._is_downloading and not self._is_downloaded):
            self.btn.setVisible(False)
            self.progress_bar.setVisible(True)
            super().leaveEvent(event)

    @property
    def get_id(self):
        return self._id
