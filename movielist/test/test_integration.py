from unittest import mock

import fakeredis
import pytest
import responses

from movielist import db
from movielist.models import Movie
from movielist.server import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@responses.activate
@mock.patch('movielist.db.redis', fakeredis.FakeRedis(decode_responses=True))
def test_get_movies(client):
    responses.add(responses.GET, 'https://ghibliapi.herokuapp.com/films', json=[
        {'id': 'mov1', 'title': 'Castle in the Sky'},
    ])
    responses.add(responses.GET, 'https://ghibliapi.herokuapp.com/people', json=[
        {'id': 'char1', 'name': 'Colonel Muska', 'films': ['https://ghibliapi.herokuapp.com/films/mov1']},
    ])
    response = client.get('/movies')
    assert response.status_code == 200
    assert b'Castle in the Sky' in response.data
    assert b'Colonel Muska' in response.data

    assert db.get_movies() == [
        Movie(id='mov1', title='Castle in the Sky', characters=['Colonel Muska']),
    ]
