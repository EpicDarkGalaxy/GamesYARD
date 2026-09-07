# GamesYARD

GamseYARD is a front-end and a scraper for downloading games from the Internet.

This repository contains a Python-based scraper and a lightweight front-end to browse and download retro and abandonware games for personal archival and educational purposes.

## Features

- Web scraper to discover and download game files from supported sources
- Simple front-end for browsing and initiating downloads
- Configuration-driven scraping targets and rules

## Requirements

- Python 3.10+
- pip

## Installation

1. Clone the repository:

   git clone https://github.com/EpicDarkGalaxy/GamesYARD.git
   cd GamesYARD

2. (Optional) Create a virtual environment and install dependencies:

   python -m venv .venv
   source .venv/bin/activate   # On Windows use `.venv\\Scripts\\activate`
   pip install -r requirements.txt

## Configuration

Store Api keys in the env file (inside root folder)


## Project structure (example)

- src/ - core Python package
- src/services/ - scrapers
- src/ui/ - All UI Code
- requirements.txt - Python dependencies

## Documentation

See DOCUMENTATION.md for detailed developer and user documentation.

## Contributing

Contributions are welcome! Please read CONTRIBUTING.md for guidelines about issues, pull requests, and the development workflow.

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0). See the LICENSE file for details.
