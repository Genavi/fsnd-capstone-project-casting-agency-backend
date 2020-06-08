import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Movie, Artist, MovieToArtist

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app, resources={r"/*": {"origins": "*"}})

  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

# ROUTES
'''
GET /movies
'''
@app.route('/movies', methods=['GET'])
def get_movies():
  try:
    movies = Movie.query.all()

    movies_list = []
    for movie in movies:
      movies_list.append(movie.format())

    return jsonify({
      'success': True,
      'movies': movies_list
    }), 200

  except Exception:
      abort(404)


'''
POST /movies
'''
@app.route('/movies', methods=['POST'])
def post_movies():
  try:
    body = request.get_json()
    if not ('title' in body and 'release_date' in body):
        abort(422)

    new_movie = body.get('title')
    new_release_date = body.get('release_date')

    movie = Movie(title=new_movie, release_date=new_release_date)
    movie.insert()

    return jsonify({
        'success': True,
        'movies': [movie.format() for movie in Movie.query.all()]
    }), 200

  except Exception:
    abort(404)


'''
PATCH /movies/<id>
'''
@app.route('/movies/<int:id>', methods=['PATCH'])
def patch_movie(id):
    try:
        body = request.get_json()
        movie = Movie.query.get(id)

        if movie is None:
            abort(404)

        if "title" in body and "title" is None or "release_date" in body and "release_date" is None:
            abort(400)

        if "title" in body:
            movie.title = body['title']

        if "release_date" in body:
            movie.release_date = body['release_date']
        
        movie.update()

        return jsonify({
            'success': True,
            'movies': [movie.format() for movie in Movie.query.all()]
        }), 200


    except Exception:
        abort(404)


'''
DELETE /movies/<id>
'''
@app.route('/movies/<id>', methods=['DELETE'])
def delete_movies(id):
    try:
        movie = Movie.query.get(id)

        if movie is None:
            abort(404)
            
        movie.delete()

        return jsonify({
            'success': True,
            'delete': id
        })
        
    except Exception:
        abort(404)