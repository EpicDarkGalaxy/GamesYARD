from PySide6.QtCore import QObject, Signal

class PresenterBridgeSignals(QObject):
    show_card = Signal(object)

PRESENTER_BRIDGE_SIGNALS = PresenterBridgeSignals()
