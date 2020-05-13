from unittest import mock

from movielist.domain import get_movie_list
from movielist.models import GhibliMovie, GhibliCharacter, Movie


@mock.patch('movielist.domain.db')
@mock.patch('movielist.domain.ghibli_client')
def test_get_movie_list_initial(ghibli_client, db):
    db.get_movies.return_value = []
    ghibli_client.get_movies.return_value = [
        GhibliMovie(id='mov1', title='title1'),
        GhibliMovie(id='mov2', title='title2'),
    ]
    ghibli_client.get_characters.return_value = [
        GhibliCharacter(name='char1', film_ids=['mov2']),
        GhibliCharacter(name='char2', film_ids=['mov2']),
    ]
    movie_list = get_movie_list()
    assert len(movie_list) == 2
    mov1, mov2 = movie_list
    assert mov1.title == 'title1'
    assert mov1.characters == []
    assert mov2.title == 'title2'
    assert mov2.characters == ['char1', 'char2']

    ghibli_client.get_movies.assert_called_once()
    ghibli_client.get_characters.assert_called_once()


@mock.patch('movielist.domain.db')
@mock.patch('movielist.domain.ghibli_client')
def test_get_movie_list_no_new_release(ghibli_client, db):
    db.get_movies.return_value = [
        Movie(id='mov1', title='title1', characters=['character']),
    ]

    ghibli_client.get_movies.return_value = [
        GhibliMovie(id='mov1', title='title1'),
    ]

    movie_list = get_movie_list()
    assert len(movie_list) == 1

    ghibli_client.get_movies.assert_called_once()
    ghibli_client.get_characters.assert_not_called()


@mock.patch('movielist.domain.db')
@mock.patch('movielist.domain.ghibli_client')
def test_get_movie_list_new_release(ghibli_client, db):
    db.get_movies.return_value = [
        Movie(id='mov1', title='title1', characters=['character']),
    ]
    ghibli_client.get_movies.return_value = [
        GhibliMovie(id='mov1', title='title1'),
        GhibliMovie(id='mov2', title='title2'),
    ]
    ghibli_client.get_characters.return_value = [
        GhibliCharacter(name='character', film_ids=['mov1', 'mov2']),
    ]
    movie_list = get_movie_list()
    assert len(movie_list) == 2
    mov1, mov2 = movie_list
    assert mov1.title == 'title1'
    assert mov1.characters == ['character']
    assert mov2.title == 'title2'
    assert mov2.characters == ['character']

    ghibli_client.get_movies.assert_called_once()
    ghibli_client.get_characters.assert_called_once()
