from PySide6.QtGui import QPixmap

class IGameView:
    def set_title(self, title: str):
        raise NotImplementedError
    def set_poster(self, poster: QPixmap):
        raise NotImplementedError
    def set_description(self, description: dict[str, str]):
        raise NotImplementedError
    def update_providers(self, providers, exlude):
        raise NotImplementedError
