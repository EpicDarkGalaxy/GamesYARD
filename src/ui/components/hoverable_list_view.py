from PySide6.QtWidgets import QListView
from PySide6.QtCore import Qt

class HoverableListView(QListView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)  # Always track mouse for hover

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.viewport().update() # Force repaint to clear hover effect when leaving the view

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.viewport().update() # Force repaint to update hover effect as mouse moves
