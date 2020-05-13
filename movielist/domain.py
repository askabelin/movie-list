from collections import defaultdict
from typing import List

from movielist import db, ghibli_client
from movielist.models import Movie


def _get_characters_mapping():
    characters_by_film_id = defaultdict(list)
    for ghibli_character in ghibli_client.get_characters():
        for film_id in ghibli_character.film_ids:
            characters_by_film_id[film_id].append(ghibli_character.name)
    return characters_by_film_id


def get_movie_list() -> List[Movie]:
    cached_movies = db.get_movies()
    ghibli_movies = ghibli_client.get_movies()

    if len(cached_movies) == len(ghibli_movies):
        # no new releases: return cached
        return cached_movies

    characters_by_film_id = _get_characters_mapping()

    movies = [Movie(
        id=gm.id,
        title=gm.title,
        characters=characters_by_film_id[gm.id]
    ) for gm in ghibli_movies]

    db.save_movies(movies)
    return movies
