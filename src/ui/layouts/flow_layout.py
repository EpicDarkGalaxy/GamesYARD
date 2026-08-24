import sys

from PySide6.QtCore import QPoint, QRect, QSize, Qt
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QLayout,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


# --- Reusable FlowLayout ---
class FlowLayout(QLayout):
    def __init__(self, parent=None, margin=-1, spacing=-1):
        super().__init__(parent)
        if parent is not None:
            self.setContentsMargins(margin, margin, margin, margin)
        self.setSpacing(spacing)
        self._item_list = []

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        self._item_list.append(item)

    def count(self):
        return len(self._item_list)

    def itemAt(self, index):
        if 0 <= index < len(self._item_list):
            return self._item_list[index]
        return None

    def takeAt(self, index):
        if 0 <= index < len(self._item_list):
            return self._item_list.pop(index)
        return None

    def expandingDirections(self):
        return Qt.Orientation.Horizontal | Qt.Orientation.Vertical

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return self._do_layout(QRect(0, 0, width, 0), test_only=True)

    def setGeometry(self, rect):
        super().setGeometry(rect)
        self._do_layout(rect, test_only=False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()
        for item in self._item_list:
            size = size.expandedTo(item.minimumSize())
        margins = self.contentsMargins()
        size += QSize(margins.left() + margins.right(), margins.top() + margins.bottom())
        return size

    def clear_layout(self):
        while self.count():
            item = self.takeAt(0)
            widget = item.widget()

            if (widget is not None):
                widget.deleteLater()
            elif(item.layout() is not None):
                item.layout().deleteLater()

    def _do_layout(self, rect, test_only):
        left, top, right, bottom = self.getContentsMargins()
        effective_rect = rect.adjusted(+left, +top, -right, -bottom)
        x = effective_rect.x()
        y = effective_rect.y()
        line_height = 0

        for item in self._item_list:
            if (hasattr(item, 'widget')):
                widget = item.widget()
            else:
                widget = item

            space_x = self.horizontalSpacing()
            if space_x == -1:
                space_x = widget.style().layoutSpacing(
                    QSizePolicy.ControlType.PushButton,
                    QSizePolicy.ControlType.PushButton,
                    Qt.Orientation.Horizontal,
                )
            space_y = self.verticalSpacing()
            if space_y == -1:
                space_y = widget.style().layoutSpacing(
                    QSizePolicy.ControlType.PushButton,
                    QSizePolicy.ControlType.PushButton,
                    Qt.Orientation.Vertical,
                )

            item_size = item.sizeHint()
            next_x = x + item_size.width() + space_x

            if next_x - space_x > effective_rect.right() and line_height > 0:
                x = effective_rect.x()
                y = y + line_height + space_y
                next_x = x + item_size.width() + space_x
                line_height = 0

            if not test_only:
                item.setGeometry(QRect(QPoint(x, y), item_size))

            x = next_x
            line_height = max(line_height, item_size.height())

        return y + line_height - rect.y() + bottom

    def horizontalSpacing(self):
        if self.spacing() >= 0:
            return self.spacing()
        return self._smart_spacing(QSizePolicy.ControlType.PushButton, Qt.Orientation.Horizontal)

    def verticalSpacing(self):
        if self.spacing() >= 0:
            return self.spacing()
        return self._smart_spacing(QSizePolicy.ControlType.PushButton, Qt.Orientation.Vertical)

    def _smart_spacing(self, control_type, orientation):
        parent = self.parent()
        if parent is None:
            return -1
        if parent.isWidgetType():
            return parent.style().layoutSpacing(control_type, control_type, orientation)
        return parent.spacing()
