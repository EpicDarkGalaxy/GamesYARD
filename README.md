# TicTikBomb

TicTikBomb is a desktop application built with PySide6 that allows users to search, browse, and fetch information about games from goldmines like internet archive.

## Features
- **Game Search**: Search for games directly from the application.
- **Game Details**: View system requirements and metadata for selected games
- **Download**: it can donwload from MediaFire and Filekeeper hosting sites.

## Requirements
- Python 3.10+
- `PySide6`
- `curl_cffi`
- `beautifulsoup4`

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/TicTikBomb.git
   cd TicTikBomb
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirement.txt
   ```

## Usage
Run the application using:
```bash
python app.py
```

## Project Structure
- `src/core/`: Contains the business logic, fetchers, and threading management.
- `src/ui/`: Contains UI design files.
- `src/windows/`: Contains the windows logic (e.g., `GameInfoWindow`).
- `app.py`: The entry point of the application.
