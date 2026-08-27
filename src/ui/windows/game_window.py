from typing import override

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QLabel,
    QWidget,
)

from ...core.tools import get_logger
from ...ui import Ui_gameinfo
from ..ui_signals import GameWindowSignals

logger = get_logger(__name__)

class GameWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 600, 600)
        self.ui = Ui_gameinfo()
        self.ui.setupUi(self)

        self.signals = GameWindowSignals()

        self.ui.fetch_btn.clicked.connect(self.fetch_btn)

    def fetch_btn(self):
        self.signals.fetch_btn_clicked.emit()

    def set_title(self, title: str):
        logger.info(f"setting title: {title}")
        self.ui.game_name_label.setText(title)

    def set_poster(self, poster: QPixmap):
        """
        Called every time the poster of the selected game is changed
        """
        logger.info("setting poster")

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
        logger.info(f"Updating providers: {providers}")
        marged_providers = providers + exlude

        self.clear_layout(self.ui.download_links_layout, exlude)
        if (not providers):
            return

        for provider in marged_providers:
            self.ui.download_links_layout.addWidget(provider)

    def clear_layout(self, layout, exclude=None):
        if exclude is None:
            exclude = []
        while layout.count():
            item = layout.takeAt(0)
            if item is None:
                continue

            widget = item.widget()
            if widget:
                if widget in exclude:
                    continue
                widget.deleteLater()
            elif item.layout():
                self.clear_layout(item.layout(), exclude)
                item.layout().deleteLater()

    def closeEvent(self, event):
        self.signals.close.emit(event)
