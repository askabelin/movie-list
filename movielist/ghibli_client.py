from typing import Iterable, List
from urllib.parse import urljoin

import requests

from movielist.models import GhibliMovie, GhibliCharacter

GHIBLI_BASE_URL = 'https://ghibliapi.herokuapp.com'
FILMS_URL = urljoin(GHIBLI_BASE_URL, 'films')
PEOPLE_URL = urljoin(GHIBLI_BASE_URL, 'people')
FETCH_LIMIT = 100


def _fetch_resource(url, fields):
    response = requests.get(url, params={'limit': FETCH_LIMIT, 'fields': ','.join(fields)})
    response.raise_for_status()
    return response.json()


def _extract_ids(urls: Iterable[str]) -> List[str]:
    return [url.split('/')[-1] for url in urls]


def get_movies() -> List[GhibliMovie]:
    movies_data = _fetch_resource(FILMS_URL, ('id', 'title'))
    return [GhibliMovie(
        id=item['id'],
        title=item['title'],
    ) for item in movies_data]


def get_characters() -> Iterable[GhibliCharacter]:
    people_data = _fetch_resource(PEOPLE_URL, ('name', 'films'))
    return [GhibliCharacter(
        name=item['name'],
        film_ids=_extract_ids(item['films']),
    ) for item in people_data]
