from dataclasses import dataclass, field

@dataclass(frozen=True)
class GameData:
    id: int = 0
    title: str = ""
    background_image: str = ""
    released: str = ""
    rating: float = 0.0
    metacritic: int = 0
    genres: list[str] = field(default_factory=list)
    description: str = ""
    poster_pixmap: object = field(default_factory=object)
    system_requirements: dict[str, str] = field(default_factory=dict)
