from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PySide6.QtCore import Signal, Qt

class ClickableLabel(QWidget):
    # Create a custom signal
    clicked = Signal()
    label_text = Signal(str, QWidget)

    def __init__(self):
        super().__init__()
        self.horizontal = QHBoxLayout(self)
        self.horizontal.setContentsMargins(0, 0, 0, 0)

        self.raw_text = ""

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.horizontal.addWidget(self.label)

    def mousePressEvent(self, event):
        # Trigger the signal when the user clicks
        self.label_text.emit(self.raw_text, self)
        super().mousePressEvent(event)
