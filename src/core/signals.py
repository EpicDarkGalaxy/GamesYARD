from dataclasses import dataclass

from PySide6.QtCore import QObject, Signal


# Singals for the worker threads

class WorkerSignals(QObject):
    fail = Signal(str)  # Signal to emit error messages
    finished = Signal()  # Signal to indicate the worker has finished

@dataclass
class IconWorkerSignals(WorkerSignals):
    icon_fetched = Signal(int, bytes)  # Signal to emit the list of fetched icons


class FetchWorkerSignals(WorkerSignals):
    fetch_finished = Signal(list)  # Signal to emit the list of fetched items
    fetch_fail = Signal() # Signal to indicate the worker has failed to fetch items
