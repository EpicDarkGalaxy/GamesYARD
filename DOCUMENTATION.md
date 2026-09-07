# GamesYARD Documentation

Welcome to the technical documentation for **GamesYARD**, a Python-based desktop application and scraping front-end designed to discover, manage, and download games from various file-hosting and archival providers.

---

## Architecture Overview

GamesYARD follows a modular, clean-separation architecture divided into core business logic, providers/scrapers, asynchronous workers, and the PySide6 user interface.

```
GamesYARD/
├── src/
│   ├── core/
│   │   ├── aio/            # Task runners and download workers
│   │   ├── managers/       # Download manager & state handlers
│   │   ├── models/         # Data models and structures
│   │   ├── services/       # Scrapers and file host providers
│   │   └── utils/          # Logging, resource path resolvers, helpers
│   └── ui/
│       ├── components/     # Reusable UI widgets & browser dialogs
│       ├── styles/         # QSS stylesheets
│       └── views/          # Main windows and application views
├── tests/                  # Test scripts and experiments
├── app.py                  # Application entry point
└── requirements.txt        # Python dependencies
```

---

## Core Modules & Components

### 1. Provider System (`src/core/services/providers/`)
Providers encapsulate the logic required to resolve landing pages or folder URLs into direct file download links and metadata (such as original filenames).
- **`BaseProvider`**: Abstract base class defining `can_handle(url)` and `extract_dl_url(url)`.
- **`GoFileProvider`**: Integrates with GoFile.io API v2. Dynamically fetches website tokens (`getjs`) and guest account tokens to prevent `notPremium` errors, while supporting multi-part folder sorting.
- **`DataVaultsProvider`**: Handles multi-step landing pages and triggers embedded browser assistance when reCAPTCHA / bot challenges are encountered.
- **`PixelDrainProvider` & `MediaFireProvider`**: Direct API and DOM-based extraction providers.
- **`ProviderFactory`**: Registry managing all active providers.

### 2. Scraper System (`src/core/services/scrapers/`)
Scrapers discover game download pages and host links based on search queries.
- **`InternetArchiveScraper`**: Uses Archive.org's official JSON search and metadata APIs with smart scoring/filtering to filter out soundtracks and manuals, returning direct download links.
- **`FourFNetScraper` & `GameBountyScraper`**: Web scrapers for game directory discovery.

### 3. Asynchronous Download Pipeline (`src/core/aio/`)
- **`DownloadWorker`**: Runs in a background thread using `curl_cffi` to perform chunked streaming downloads with TLS fingerprint impersonation (`chrome124`). Supports:
  - Automatic `HEAD` checks to detect if a file is already fully downloaded.
  - HTTP `Range` request resumption (`206 Partial Content`).
  - Fallbacks for servers ignoring range headers (`200 OK`).
  - Accurate progress calculation, ETA estimation, and stuck-at-99% fix.

### 4. Embedded CAPTCHA Browser (`src/ui/components/browser_dialog.py`)
- **`CaptchaBrowserDialog`**: A PySide6 `QWebEngineView` dialog equipped with an ad-blocking request interceptor and popup blocker. Allows users to solve reCAPTCHA challenges interactively inside the application while blocking ad redirects (e.g. YouTube/adware popups).

---

## Building and Packaging (PyInstaller)

To package GamesYARD into a standalone executable:

```bash
pyinstaller --noconsole --onefile --add-data "src:src" app.py
```

### Resource Path Resolution
When packaged with PyInstaller, assets like stylesheets (`style.qss`) and icons should be loaded using the `sys._MEIPASS` or `sys.executable` path helper:

```python
import sys
import os

def resource_path(relative_path: str) -> str:
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
```

---

## Configuration & Environment

- **`requirements.txt`**: Contains dependencies including `PySide6`, `PySide6-WebEngine`, `curl_cffi`, and `beautifulsoup4`.
- **Logging**: Configured via `src/core/utils/log.py` writing runtime logs to `app.log`.

---

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0). See `LICENSE` for details.
