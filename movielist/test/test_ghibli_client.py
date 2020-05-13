import responses

from movielist.ghibli_client import get_movies, get_characters
from movielist.models import GhibliMovie, GhibliCharacter


@responses.activate
def test_get_movies():
    responses.add(responses.GET, 'https://ghibliapi.herokuapp.com/films', json=[
        {'id': 'mov1', 'title': 'Castle in the Sky'},
        {'id': 'mov2', 'title': 'Porco Rosso'},
    ])
    movies = get_movies()
    assert movies == [
        GhibliMovie(id='mov1', title='Castle in the Sky'),
        GhibliMovie(id='mov2', title='Porco Rosso'),
    ]


@responses.activate
def test_get_characters():
    responses.add(responses.GET, 'https://ghibliapi.herokuapp.com/people', json=[
        {'id': 'char1', 'name': 'Colonel Muska', 'films': ['https://ghibliapi.herokuapp.com/films/mov1']},
        {'id': 'char2', 'name': 'Porco Rosso', 'films': ['https://ghibliapi.herokuapp.com/films/mov2']},
    ])
    characters = get_characters()
    assert characters == [
        GhibliCharacter(name='Colonel Muska', film_ids=['mov1']),
        GhibliCharacter(name='Porco Rosso', film_ids=['mov2']),
    ]
