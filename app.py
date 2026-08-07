import sys
from src.core.log import get_logger
from src.core.utils import get_img_data
from src.core.fetcher import GameFetcher
from src.windows.gameInfo import GameInfoWindow
from src.core.asynchronus.thread import (
    IconFetchWorker, FetchWorker, Worker
)
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QGridLayout,
    QListWidgetItem,
    QToolBar, QLineEdit, QListWidget, QLabel, QPushButton as QButton
)
from PySide6.QtCore import (
    QThreadPool, Qt, Slot, QSize, QThread,  QRunnable
)
from PySide6.QtGui import ( QIcon, QPixmap )

logger = get_logger(__name__)
worker = None

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("4fnet FrontEnd")
        self.resize(500, 400)


        self.gf = GameFetcher()
        self.search_query = ""

        # --------------------------------------------------
        # 1. Central Layout (List of Items)
        # --------------------------------------------------
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QGridLayout(central_widget)

        # Toolbar
        toolbar = QToolBar("Search")
        toolbar.setMovable(False)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        # SearchBar
        self.searchBar = QLineEdit()
        self.searchBar.setPlaceholderText("Search Game")
        self.searchBar.setClearButtonEnabled(True)
        self.searchBar.returnPressed.connect(self.handle_search)
        toolbar.addWidget(self.searchBar)

        # Fetch Button
        self.fetch_btn = QButton("FETCH", self)
        self.status = QLabel("Ready")
        self.fetch_btn.clicked.connect(self.handle_search)
        toolbar.addWidget(self.fetch_btn)
        toolbar.addWidget(self.status)

        # Games List (Main Content)
        self.items_list = QListWidget()
        self.items_list.setViewMode(QListWidget.IconMode)
        self.items_list.setResizeMode(QListWidget.Adjust)
        self.items_list.setIconSize(QSize(150, 150))
        self.items_list.setGridSize(QSize(160, 210))
        self.items_list.setSpacing(10)
        self.items_list.setWordWrap(True)
        self.items_list.clicked.connect(self.on_item_clicked)
        self.items_list.setMovement(QListWidget.Movement.Static)
        layout.addWidget(self.items_list)

    @Slot()
    def on_item_clicked(self, index):
        selected_game = self.gf.gameList[index.row()]
        print(f"Selected Game: {selected_game.title}")
        game_details = self.gf.get_game_details(selected_game)

        # Create and show the GameInfoWindow with the fetched details
        print(f"from MainWindow {game_details.href}")
        self.game_info_window = GameInfoWindow(game_details)
        self.game_info_window.show()

    @Slot()
    def handle_search(self):
        self.items_list.clear() # Clear the list before fetching new items
        self.fetch_btn.setEnabled(False) # Disable the fetch_btn to prevent multiple fetches
        self.status.setText("Fetching...")

        self.search_query = self.searchBar.text().strip() # Get the search query from the search bar

        # Start the fetch game_fetch_worker thread
        self.game_fetch_worker = FetchWorker(self.search_query, self.gf)
        self.game_fetch_worker.signals.fetch_finished.connect(self.on_fetch_finished)
        self.game_fetch_worker.signals.fetch_fail.connect(self.on_fetch_fail)  # Re-enable the fetch_btn on failure
        self.game_fetch_worker.finished.connect(self.game_fetch_worker.deleteLater)
        self.game_fetch_worker.start()

# ---------------------------
#  On_x (Signals)
# ---------------------------
    def on_fetch_fail(self):
        self.fetch_btn.setEnabled(True)
        self.status.setText("Failed!")

    def on_fetch_finished(self, items):     
        worker.clear_thread_pool()

        print("Fetch finished, updating UI...")
        self.fetch_btn.setEnabled(True)
        self.status.setText("Fetch Complete")

        # Add items to the list and start fetching icons
        for index, game in enumerate(items):
            item = QListWidgetItem(get_default_icon(), game.title)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.items_list.addItem(item)

            print(f"Added item: {game.title} at index {index}")

            # Start fetching the icon for this item in a separate thread
            icon_fetch_task = IconFetchWorker(index, game.posterLink)
            icon_fetch_task.signals.icon_fetched.connect(self.on_icons_fetched)
            worker.add_to_pool(icon_fetch_task)

    def on_icons_fetched(self, index: int, img_data: bytes):
        print("Icon fetched, updating UI...")
        pixmap = QPixmap()
        pixmap.loadFromData(img_data)

        print(f"Setting icon for item at index {index}...")
        item = self.items_list.item(index)

        self.gf.gameList[index].posterPixmap = pixmap  # Store the QPixmap in the gameList
        if item:
            item.setIcon(QIcon(pixmap))
# ---------------------------
# On_X (Sigals) ends here  
# ---------------------------

def get_default_icon():
    pixmap = QPixmap(150, 150)
    pixmap.fill(Qt.GlobalColor.lightGray)
    return QIcon(pixmap)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    worker = Worker()
    sys.exit(app.exec())
