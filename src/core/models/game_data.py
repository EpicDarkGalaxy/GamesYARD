from dataclasses import dataclass, field

@dataclass
class GameData:
    id: int
    title: str
    background_image: str | None
    released: str | None
    rating: float
    metacritic: int | None
    genres: list[str] = field(default_factory=list)
    description: str = ""
    poster_pixmap: object = None
    system_requirements: dict | None = None
