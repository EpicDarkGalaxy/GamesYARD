from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QLabel, QWidget, QFileDialog, QProgressBar, QHBoxLayout, QStyleFactory

from ...core.tools import get_logger
from ...core import MANAGER
from ...ui import Ui_gameinfo
from ..widget.provider_button_widget import ProviderButton

logger = get_logger(__name__)

class GameInfoWindow(QWidget):
    def __init__(self, game_card):
        super().__init__()

        self.setWindowTitle(f"Game Info - {game_card.title} ")
        self.setGeometry(100, 100, 600, 600)

        self.game_card = game_card
        self.links: list[ProviderButton] = []
        self.progress_bars: list[QProgressBar] = []

        self.ui = Ui_gameinfo()
        self.ui.setupUi(self)
        self.ui.fetch_btn.clicked.connect(self.on_fetch)
        self.ui.game_name_label.setText(game_card.title)

        self.set_poster(game_card.poster_pixmap)
        self.set_details(game_card.details.system_requirements)

    def set_poster(self, pixmap):
        if (pixmap):
            self.ui.game_poster.setPixmap(pixmap)

    def set_details(self, details):
        logger.info("setting details")

        for catg, req in details.items():
            label = QLabel()
            label.setText(f"<b>{catg}</b>: {req}")
            self.ui.game_details_layout.addWidget(label)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())
                item.layout().deleteLater()

    @Slot()
    def on_fetch(self):
        if (not self.game_card.details):
            return

        self.links.clear()
        self.clear_layout(self.ui.download_links_layout)

        download_links = MANAGER.request_provider_links(self.game_card.url)
        for link in download_links:
            name = MANAGER.request_provider_name(link)
            label = ProviderButton(name, link, self.on_provider_click)
            label.setProperty("styleClass","provider-link-label")

            # label.btn.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            # label.btn.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

            self.links.append(label) # Storing a Reference to keep it alive
            self.ui.download_links_layout.addWidget(label)
            self.game_card.details.downloads_links.append(link)


    # Its a temporary function and maybe be get removed
    @staticmethod
    def set_link_state(state: bool, label: ProviderButton):
        label.setInteraction(state)

    # @Slot(float)
    # def on_progress(self, progress):
    #     logger.info(f"downloading {progress}%")
    #     self.progress_bar.setValue(float(progress))

    # I will change it
    @Slot(str, object)
    def on_provider_click(self, provider_link, label: ProviderButton):
        logger.info(f"Clicked Link: {provider_link}")

        # Disable Link so the user can't spam it
        self.set_link_state(False, label)

        file_path = QFileDialog.getSaveFileName(self, "Save File", "game.exe")
        if (file_path):
            MANAGER.download_game(file_path[0], provider_link, label.update_progress)

    # @Slot()
    # def on_download_finished():
    #     pass
