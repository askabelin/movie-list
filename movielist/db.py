import os
from typing import Iterable, List

from redis import Redis
from fakeredis import FakeRedis

from movielist.models import Movie

redis_class = FakeRedis if os.environ.get('USE_IN_MEMORY_REDIS') == '1' else Redis
redis = redis_class(decode_responses=True)


def save_movies(movies: Iterable[Movie]) -> None:
    with redis.pipeline() as pipe:
        for movie in movies:
            pipe.hset(movie.id, 'title', movie.title)
            pipe.hset(movie.id, 'characters', '\n'.join(movie.characters))
        pipe.execute()


def get_movies() -> List[Movie]:
    keys = redis.keys()
    with redis.pipeline() as pipe:
        for key in keys:
            pipe.hgetall(key)
        values = pipe.execute()

    return [Movie(
        id=movie_id,
        title=movie_data['title'],
        characters=movie_data['characters'].split('\n')
    ) for movie_id, movie_data in zip(keys, values)]
