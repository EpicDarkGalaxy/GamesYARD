# GamesYARD

GamesYARD is a desktop application built with PySide6 that lets users search, browse, and download classic/archived games from sources such as the Internet Archive and supported file hosts (e.g., MediaFire, Filekeeper).

## Features
- **Game Search**: Search for games directly from the application.
- **Game Details**: View system requirements and metadata for selected games.
- **Download**: Resolve provider landing pages to direct links and download in the background.

## Requirements
- Python 3.10+
- PySide6
- curl_cffi
- beautifulsoup4 (bs4)
- pyinstaller (optional, for building standalone binaries)

## Installation
1. Clone the repository:
```bash
git clone https://github.com/EpicDarkGalaxy/GamesYARD.git
cd GamesYARD
```
2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
# macOS / Linux
source venv/bin/activate
# Windows (PowerShell)
# .\venv\Scripts\Activate.ps1
# Windows (cmd)
# venv\Scripts\activate
pip install -r requirements.txt
```

## Usage
Run the application with:
```bash
python app.py
```

## Project structure (top-level)
- `app.py` — application entrypoint; creates QApplication and wires Manager, presenters, and windows
- `requirements.txt` — Python dependencies
- `src/core/` — business logic, downloaders, fetchers, worker/threads
- `src/ui/` — generated Qt UI files, presenters, controllers, style.qss
- `ui_design/` — design assets and layouts

## Notes / Known issues
- The repository contains a few internal names and directories (e.g., `src/core/asynchronus`) whose spelling may look inconsistent; this does not affect how to run the app.

## Contributing
Feel free to open issues or pull requests for bug fixes, new provider implementations in `src/core/downloaders/`, or UI improvements.
