from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QStyleFactory,
    QWidget,
)

from ...core import MANAGER
from ...core.tools import get_logger
from ...ui import Ui_gameinfo
from ..widget.provider_button_widget import ProviderButton

logger = get_logger(__name__)

class GameInfoWindow(QWidget):
    def __init__(self):
        super().__init__()
        MANAGER.game_info_signals.game_selected.connect(self.on_game_selected)

        self.setGeometry(100, 100, 600, 600)

        self.links: list[ProviderButton] = []
        self.progress_bars: list[QProgressBar] = []

        self.ui = Ui_gameinfo()
        self.ui.setupUi(self)
        self.ui.fetch_btn.clicked.connect(self.on_fetch)

    @Slot(object)
    def on_game_selected(self, game_data):
        self.game_card=game_data
        title = game_data.title
        pixmap = game_data.poster_pixmap
        details = game_data.details.system_requirements

        self.set_title(title)
        self.set_poster(pixmap)
        self.set_details(details)
        self.setWindowTitle(f"Game Info - {title}")

    def set_title(self, title):
        self.ui.game_name_label.setText(title)

    def set_poster(self, pixmap):
        print("Loading thumb")
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
    def on_provider_click(self, landing_page_url, provider_btn: ProviderButton):
        logger.info(f"Clicked Link: {landing_page_url}")

        # Disable Link so the user can't spam it
        self.set_link_state(False, provider_btn)

        suggested_name = MANAGER.request_filename_from_url(landing_page_url)
        file_path = QFileDialog.getSaveFileName(self, "Save Game", suggested_name)
        if (file_path[0] != ""):
            MANAGER.resolve_and_download(file_path[0], landing_page_url, provider_btn.update_progress)
        else:
            return
    # @Slot()
    # def on_download_finished():
    #     pass
