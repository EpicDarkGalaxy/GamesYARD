from PySide6.QtCore import Signal
from PySide6.QtWidgets import QHBoxLayout, QProgressBar, QPushButton, QWidget
from uuid import uuid4
from ...core.tools.log import get_logger

logger = get_logger(__name__)


class ProviderButton(QWidget):
    download_requested = Signal(str, str) # URL, Widget reference
    cancel_requested = Signal(str, str) # self, provider_id

    _is_downloading = False
    _is_downloaded = False
    has_download_failed = False

    def __init__(self, provider_name: str="", provider_url: str=""):
        super().__init__()
        self._id = str(uuid4())
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.provider_name = provider_name
        self.provider_url = provider_url

        self.btn = QPushButton(provider_name)
        self.btn.setObjectName("provider-btn")
        self.btn.clicked.connect(self.handle_click)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setVisible(False) # Hide by default!

        # Put them side-by-side or let progress_bar replace the button space
        self.main_layout.addWidget(self.btn)
        self.main_layout.addWidget(self.progress_bar)

    def handle_click(self):
        if (self._is_downloading):
            print(f"Requesting cancellation: {self.provider_url}")
            self.set_downloading_state()
            self.cancel_requested.emit(self.provider_url, self._id)
        else:
            print(f"Requesting download: {self.provider_url}")
            # self.set_downloading_state(True)
            self.download_requested.emit(self.provider_url, self._id)

    def update_progress(self, value: int):
        self.progress_bar.setValue(value)

    def set_downloading_state(self, is_downloading: bool=False, is_downloaded: bool=False, failed: bool=False ):
        self._is_downloading = is_downloading
        self._is_downloaded = is_downloaded
        self.has_download_failed = failed

        if (is_downloading):
            self._set_working_display()
        elif (is_downloaded):
            self._set_finished_display()
        elif (failed):
            self._set_failed_display()
        else:
            self.btn.setVisible(True)
            self.btn.setStyleSheet("")
            self.btn.setText(self.provider_name)
            self.progress_bar.setVisible(False)

    def _set_working_display(self):
        self.btn.setVisible(False)
        self.btn.setText("Downloading...")
        self.progress_bar.setVisible(True)

    def _set_finished_display(self):
        self.btn.setVisible(True)
        self.btn.setStyleSheet("""
            QPushButton {
                background-color: green;
            }
            """)
        self.btn.setText("Donwload completed, click to redownload")
        self.btn.setVisible(True)
        self.progress_bar.setVisible(False)

    def _set_failed_display(self):
        self.btn.setVisible(True)
        self.btn.setStyleSheet("""
            QPushButton {
                background-color: darkred;
            }
            """)
        self.btn.setText("Download FAILED!, click to redownload")
        self.progress_bar.setVisible(False)

    def enterEvent(self, event):
        logger.debug(
            "\n--- ProviderButton Event ---\n"
            f"ID:           {self._id}\n"
            f"Name:         {self.provider_name}\n"
            f"Downloading:  {self._is_downloading}\n"
            f"Downloaded:   {self._is_downloaded}\n"
            f"Failed:       {self.has_download_failed}\n"
            "----------------------------"
        )
        if (self._is_downloading and not self._is_downloaded and not self.has_download_failed):
            self.btn.setStyleSheet("""
                QPushButton {
                    background-color: red;
                }
                """)
            self.btn.setText("Click to Cancle")
            self.progress_bar.setVisible(False)
            self.btn.setVisible(True)
            super().enterEvent(event)

    def leaveEvent(self, event):
        if (self._is_downloading and not self._is_downloaded):
            self.btn.setVisible(False)
            self.progress_bar.setVisible(True)
            super().leaveEvent(event)

    @property
    def get_id(self):
        return self._id
