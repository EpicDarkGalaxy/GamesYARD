from PySide6.QtGui import QColor, QIcon, QPixmap


def get_default_icon() -> QPixmap:
    pixmap = QPixmap(150,150)
    pixmap.fill(QColor("lightgray"))
    return pixmap


def download_icon(url: str, get_img_data_func) -> QIcon:
    img_data = get_img_data_func(url)
    if img_data:
        pixmap = QPixmap()
        pixmap.loadFromData(img_data)
        return QIcon(pixmap)
    return QIcon(get_default_icon())


def format_speed(bytes_per_sec: float) -> str:
    if bytes_per_sec < 1024:
        return f"{bytes_per_sec:.1f} B/s"
    elif bytes_per_sec < 1024 * 1024:
        return f"{bytes_per_sec / 1024:.1f} KB/s"
    else:
        return f"{bytes_per_sec / (1024 * 1024):.1f} MB/s"


def format_eta(seconds: float) -> str:
    if seconds < 60:
        return f"{seconds:.1f} seconds"
    elif seconds < 3600:
        return f"{seconds / 60:.1f} minutes"
    elif seconds < 86400:
        return f"{seconds / 3600:.1f} hours"
    else:
        return f"{seconds / 86400:.1f} days"
