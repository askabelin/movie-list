from flask import Flask, render_template
from flask_caching import Cache

from movielist import domain


app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})


@app.route('/movies', methods=['GET'])
@cache.cached(timeout=60)
def movies():
    movie_list = domain.get_movie_list()
    return render_template('movies.html', movies=movie_list)
