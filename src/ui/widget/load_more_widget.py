from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget


class LoadMoreButtonWidget(QWidget):
    clicked = Signal()

    def __init__(self, on_click=None):
        super().__init__()

        self.setFixedSize(160, 180)

        self.main_layout = QVBoxLayout(self)

        self.btn = QPushButton("LoadMore")

        if (on_click):
            self.btn.clicked.connect(on_click)

        self.card_thumbnail = QLabel()

        self.main_layout.addWidget(self.btn)
