from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QStyleFactory,
    QWidget,
)

from PySide6.QtGui import QPixmap

from ..views.igame_view import IGameView
from ..ui_signals import GameWindowSignals

from ...core.tools import get_logger
from ...ui import Ui_gameinfo
from ..widget.provider_button_widget import ProviderButton

logger = get_logger(__name__)

class GameWindow(QWidget, IGameView):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 600, 600)
        self.ui = Ui_gameinfo()
        self.ui.setupUi(self)

        self.signals = GameWindowSignals()

        # self.ui.fetch_btn.clicked.connect(self.on_fetch_btn)

    def display_game_info(self, game_id: int):
        pass

    def set_title(self, title: str):
        pass

    def set_poster(self, poster: QPixmap):
        """
        Called every time the poster of the selected game is changed
        """
        print("Loading thumb")
        if (poster):
            self.ui.game_poster.setPixmap(poster)
        # else:
        #     self.ui.game_poster.setText("NO GAME PHOTO")
        #     self.ui.game_poster.setAlignment(Qt.AlignCenter)

    def set_description(self, description: dict[str, str]):
        logger.info("setting details")
        for catg, req in description.items():
            label = QLabel()
            label.setText(f"<b>{catg}</b>: {req}")
            self.ui.game_details_layout.addWidget(label)

    def update_providers(self, providers, exlude):
        self.clear_layout(self.ui.download_links_layout, exlude)
        if (not providers):
            return

        for provider in providers:
            self.ui.download_links_layout.addWidget(provider)

    def clear_layout(self, layout, exclude=[]):
        while layout.count():
            item = layout.itemAt(0)
            if item is not None:
                if item.widget() and item.widget() not in exclude:
                    item.widget().deleteLater()
                elif item.layout():
                    self.clear_layout(item.layout())
                    item.layout().deleteLater()
            layout.removeItem(item)
