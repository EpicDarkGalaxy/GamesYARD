from typing import Callable
from src.core.services.scrapers import (
    FourFNetScraper,
    GameBountyScraper,
    InternetArchiveScraper,
)


def discover(task_runner, game_title: str, on_complete: Callable[[dict], None]):
    """Discover provider URLs for a game title using multiple scrapers.

    This function orchestrates scraper tasks via the provided task_runner and
    calls on_complete(provider_dict) when all scrapers have finished.
    """
    scrapers = [FourFNetScraper(), GameBountyScraper(), InternetArchiveScraper()]
    provider_aggregate = {}
    pending = { 'count': len(scrapers) }

    def _on_scraper_done():
        pending['count'] -= 1
        if pending['count'] <= 0:
            on_complete(provider_aggregate)

    def _handle_providers(providers: dict):
        if isinstance(providers, dict):
            provider_aggregate.update(providers)
        _on_scraper_done()

    def _handle_game_page(game_url: str | None, scraper):
        if not game_url:
            _on_scraper_done()
            return
        task_runner.run_task(
            scraper.scrape_download_urls,
            _handle_providers,
            game_url,
        )

    for scraper in scrapers:
        task_runner.run_task(
            scraper.find_game_url,
            _handle_game_page,
            game_title,
            return_value=scraper,
        )
