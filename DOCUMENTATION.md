# GamesYARD Documentation

This document provides user-facing and developer-facing documentation for GamesYARD: installation, configuration, usage, and how to extend the project.

## Overview

GamesYARD is a Python-based scraper and front-end that helps discover and download retro and abandonware game files from supported sources. The scraper is configurable to support different targets and file-hosting layouts.

## Architecture

- Scraper: responsible for fetching listing pages, parsing game entries, and downloading files according to configured rules.
- Front-end: a small web or terminal UI that lists discovered games, shows details, and triggers downloads.
- Configuration: YAML or JSON files that specify targets, parsing rules, output directories, and rate limits.

## Installation

See README.md for quick start. In short:

1. Clone the repository.
2. Create a virtual environment and install dependencies.
3. Copy and edit the example configuration.

## Configuration

Typical configuration options (example keys):

- targets: list of websites to scrape
  - url: base URL
  - list_selector: CSS selector or XPath for game listings
  - detail_selector: selectors for title, download link, metadata
  - rate_limit: requests per second
- output_dir: where downloaded files will be stored
- user_agent: custom User-Agent header for requests
- retry: number of retries for failed downloads

## Usage

Run the scraper:

  python -m gamesyard.scraper

Options you might expect:

- `--config path` — path to configuration file (default: `config.yml`)
- `--dry-run` — run the scraper without downloading files (useful for testing parsing)
- `--limit N` — limit the number of games to process

Start the front-end (if included):

  python -m gamesyard.frontend

## Extending the scraper

- Add or update a target in the configuration with the appropriate selectors.
- If a site requires custom parsing, add a new parser module under `src/scraper/parsers/` and register it in the configuration.
- Respect robots.txt and the terms of service of target sites. Only use the scraper where you are permitted to.

## Testing

- Add unit tests to `tests/` and run them with pytest or your chosen test runner.

## Troubleshooting

- If downloads fail, check network connectivity and target site availability.
- Use `--dry-run` to validate parsing selectors without downloading.
- Check logs or increase logging verbosity for debugging.

## Legal and ethical

- Use GamesYARD only to download content you have the right to access. The maintainers are not responsible for misuse.
- Follow the target website's terms of use and copyright laws.

## Contact and contribution

See CONTRIBUTING.md for guidelines on contributing. Open issues or pull requests for bugs and improvements.
