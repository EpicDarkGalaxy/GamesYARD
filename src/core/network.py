from PySide6.QtNetwork import QNetworkAccessManager

class NetworkManager:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            # We initialize it only once
            cls._instance = QNetworkAccessManager()
        return cls._instance
