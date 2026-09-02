class BaseScraper:
    def __init__(self) -> None:
        pass

    def scrap_download_urls(self, game_name: str) -> dict[str, str]: ...
