# GamesYARD

GamesYARD is a Python-based desktop frontend and scraper for discovering and downloading games from supported file-sharing and archival providers.

---

## Features

- **Multi-Provider Support**: Integrated download extraction for GoFile.io, PixelDrain, MediaFire, DataVaults, and more.
- **Archive.org Integration**: Official API-based search and metadata scraper with intelligent scoring to filter out soundtracks and manuals.
- **Embedded CAPTCHA Browser (`QWebEngineView`)**: Clean ad-blocking and popup-blocking browser dialog to solve reCAPTCHA challenges interactively without leaving the app.
- **Robust Download Manager**: Chunked streaming downloads with TLS fingerprint impersonation (`curl_cffi`), automatic range request resumption, already-downloaded file detection, and 99% progress fix.
- **PySide6 Frontend**: Modern UI with QSS styling and async task workers.

---

## Requirements

- Python 3.10+
- PySide6 & PySide6-WebEngine
- curl_cffi

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/EpicDarkGalaxy/GamesYARD.git
   cd GamesYARD
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Windows use `.venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

---

## Building an Executable (PyInstaller)

To package GamesYARD into a standalone executable:
```bash
pyinstaller --noconsole --onefile --add-data "src:src" app.py
```

---

## Documentation

See [`DOCUMENTATION.md`](DOCUMENTATION.md) for detailed architecture, module breakdowns, and developer guides.

---

## Contributing

Contributions are welcome! Please read `CONTRIBUTING.md` for guidelines about issues, pull requests, and development workflows.

---

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0). See the `LICENSE` file for details.
