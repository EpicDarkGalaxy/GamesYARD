from PySide6.QtCore import QObject, Signal


# Singals for the worker threads
class WorkerSignals(QObject):
    fail = Signal()  # Signal to emit error messages
    finished = Signal()  # Signal to indicate the worker has finished
    cancelled = Signal()  # Signal to indicate the worker has been cancelled
    progress = Signal(float)  # Signal to emit progress updates

class ThumbnailWorkerSignals(WorkerSignals):
    thumbnail_fetch_finished = Signal(object, bytes)  # Signal to emit the list of fetched icons

class SearchWorkerSignals(WorkerSignals):
    search_finished = Signal(list)  # Signal to emit the list of fetched items
    fetch_fail = Signal() # Signal to indicate the worker has failed to fetch items

class DownloadWorkerSignals(WorkerSignals):
    download_finished = Signal(str)  # Signal to indicate the download has finished
    download_fail = Signal(str)  # Signal to indicate the download has failed
    download_progress = Signal(str, int) # Sisnal to indicate download progress for spcific id

class UrlExtractorWorkerSignals(WorkerSignals):
    link_extracted = Signal(str, str)  # Signal to emit the extracted link and the URL
