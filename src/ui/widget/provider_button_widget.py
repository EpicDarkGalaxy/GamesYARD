from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QProgressBar
from PySide6.QtCore import Signal, Qt

class ProviderButton(QWidget):
    clicked = Signal()
    special_click = Signal(str, QWidget) # I could not think of a better name!

    # _disable_interaction = False

    def __init__(self, provider_name: str, provider_link: str="", on_click=None):
        super().__init__()

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.provider_link = provider_link

        self.btn = QPushButton(self)
        self.btn.setText(provider_name)
        self.btn.clicked.connect(self.emit_special_click)
        self.btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                font-weight: bold;
            }

            QPushButton:hover {
                border: 1px solid;
            }
        """)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.adjustSize()

        self.btn_layout = QHBoxLayout(self.btn)
        self.btn_layout.setContentsMargins(0, 0, 0, 0)

        self.main_layout.addWidget(self.btn)
        self.btn_layout.addWidget(self.progress_bar)

        if (on_click):
            self.special_click.connect(on_click)

    def update_progress(self, value: int):
        self.progress_bar.setValue(value)

    def emit_special_click(self):
        self.special_click.emit(self.provider_link, self)

    # def mousePressEvent(self, event):
    #     print("Mouse Clicked")
    #     if (event.button() is Qt.MouseButton.LeftButton and not self._disable_interaction):
    #         self.special_click.emit(self.raw_text, self)
    #         super().mousePressEvent(event)

    def setInteraction(self, value: bool):
        # self._disable_interaction = value
        self.btn.setEnabled(value)
