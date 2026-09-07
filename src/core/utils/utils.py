# Compatibility wrapper to export commonly-used helpers from the utils package.
# This file keeps previous imports working while code is refactored into smaller modules.

from .log import get_logger
from .network import (
    get_img_data,
    parseHtml,
    get_direct_link,
    get_filename_for_url,
    headers,
)
from .file_utils import (
    clean_filename,
    get_default_download_dir,
    resource_path,
)
from .ui_helpers import (
    get_default_icon,
    download_icon,
    format_speed,
    format_eta,
)
from .parse_helpers import (
    decodeBase64,
    get_site_name,
)

__all__ = [
    "get_logger",
    "get_img_data",
    "parseHtml",
    "get_direct_link",
    "get_filename_for_url",
    "headers",
    "clean_filename",
    "get_default_download_dir",
    "resource_path",
    "get_default_icon",
    "download_icon",
    "format_speed",
    "format_eta",
    "decodeBase64",
    "get_site_name",
]
