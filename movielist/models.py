from dataclasses import dataclass
from typing import List


@dataclass
class GhibliCharacter:
    name: str
    film_ids: List[str]


@dataclass
class GhibliMovie:
    id: str
    title: str


@dataclass
class Movie:
    id: str
    title: str
    characters: List[str]
