from PySide6.QtCore import Qt, Signal, QUrl
from PySide6.QtNetwork import QNetworkCookie
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineUrlRequestInterceptor
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel

class CaptchaBrowserDialog(QDialog):
    # Emit tuple: (download_url, cookies_dict)
    download_intercepted = Signal(str, dict)

    def __init__(self, url: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Solve CAPTCHA / Download")
        self.resize(900, 700)

        layout = QVBoxLayout(self)
        self.info_label = QLabel("Complete the CAPTCHA to acquire download session:")
        self.info_label.setSizePolicy(Qt.Expanding, Qt.Fixed)
        layout.addWidget(self.info_label)

        self.web_view = QWebEngineView(self)

        # Access cookie store to extract session tokens/cookies after CAPTCHA is solved
        self.profile = self.web_view.page().profile()
        self.cookie_store = self.profile.cookieStore()

        layout.addWidget(self.web_view)
        self.web_view.setUrl(QUrl(url))
        self.web_view.urlChanged.connect(self._on_url_changed)

    def _on_url_changed(self, url: QUrl):
        url_str = url.toString()
        print(f"Browser navigated to: {url_str}")

        # Once the user solves CAPTCHA and reaches the final download trigger or direct link
        if any(ext in url_str.lower() for ext in [".zip", ".rar", ".7z", ".exe", ".iso", "download"]) and "datavaults.co" not in url_str:
            # Grab all current cookies from the profile store
            cookies_dict = {}

            # Synchronously collect cookies (or use cookieStore callback)
            def handle_cookie(cookie: QNetworkCookie):
                name = cookie.name().data().decode('utf-8')
                value = cookie.value().data().decode('utf-8')
                cookies_dict[name] = value

            # Note: PySide6 cookieStore loadAll + getAllCookies or synchronous grab
            self.cookie_store.loadAll()

            # Emit the intercepted direct URL and captured cookies/tokens
            self.download_intercepted.emit(url_str, cookies_dict)
            self.accept()
