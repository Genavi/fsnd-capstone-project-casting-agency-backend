import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Movie, Actor, movieActor, db
from auth import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app, resources={r"/*": {"origins": "*"}})

  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)


# FUNCTIONS
'''
Function to add castmembers to a movie
'''
def add_movie_cast(movie_id, actor_id):
  try:
    movie = Movie.query.get(movie_id)
    actor = Actor.query.get(actor_id)
    
    if movie is None:
      abort(404)
    
    if actor is None:
      abort(404)

    movie.cast.append(actor)

  except Exception as e:
    print(e)
    abort(404)


'''
Function to delete castmembers from a movie
'''
def delete_movie_cast(movie_id, actor_id):
  try:
    movie = Movie.query.get(movie_id)
    actor = Actor.query.get(actor_id)
    
    if movie is None:
      abort(404)

    if actor is None:
      abort(404)

    movie.cast.remove(actor)

  except Exception as e:
    print(e)
    abort(404)


# ROUTES
'''
GET /movies
'''
@app.route('/movies', methods=['GET'])
@requires_auth('get: movies')
def get_movies(jwt):
  try:
    return jsonify({
      'success': True,
      'movies': [movie.format() for movie in Movie.query.all()]
    }), 200

  except Exception as e:
    print(e)
    abort(404)


'''
POST /movies
'''
@app.route('/movies', methods=['POST'])
@requires_auth('post: movies')
def post_movies(jwt):
  try:
    body = request.get_json()
    if not ('title' in body and 'release_date' in body):
      abort(422)

    new_movie = body.get('title')
    new_release_date = body.get('release_date')

    movie = Movie(title=new_movie, release_date=new_release_date)
    movie.insert()

    return jsonify({
      'success': True
    }), 200

  except Exception:
    abort(404)


'''
PATCH /movies/<id>
'''
@app.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('patch: movies')
def patch_movie(jwt, movie_id):
  try:
    body = request.get_json()
    movie = Movie.query.get(movie_id)

    if movie is None:
      abort(404)

    if "title" in body and "title" is None or "release_date" in body and "release_date" is None:
      abort(400)

    if "title" in body:
      movie.title = body['title']

    if "release_date" in body:
      movie.release_date = body['release_date']

    if "cast" in body:
      cast = body['cast']

      ids = [actor['id'] for actor in cast if type(actor) is not int]
      for actor in movie.cast:
        if actor.id not in (ids):
          delete_movie_cast(movie_id, actor.id)

      for actor in cast:
        if type(actor) is int:
          add_movie_cast(movie_id, actor)

    movie.update()

    return jsonify({
      'success': True
    }), 200

  except Exception as e:
    print(e)
    abort(404)


'''
DELETE /movies/<id>
'''
@app.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete: movies')
def delete_movies(jwt, movie_id):
  try:
    movie = Movie.query.get(movie_id)

    if movie is None:
      abort(404)
        
    movie.delete()

    return jsonify({
      'success': True
    })
      
  except Exception as e:
    abort(404)


'''
GET /actors
'''
@app.route('/actors', methods=['GET'])
@requires_auth('get: actors')
def get_actors(jwt):
  try:
    return jsonify({
      'success': True,
      'actors': [actor.format() for actor in Actor.query.all()]
    }), 200

  except Exception:
    abort(404)


'''
POST /actors
'''
@app.route('/actors', methods=['POST'])
@requires_auth('post: actors')
def post_actors(jwt):
  try:
    body = request.get_json()
    if not ('name' in body and 'age' in body and 'gender' in body):
      abort(422)

    new_name = body.get('name')
    new_age = body.get('age')
    new_gender = body.get('gender')

    actor = Actor(name=new_name, age=new_age, gender=new_gender)
    actor.insert()

    return jsonify({
      'success': True
    }), 200

  except Exception as e:
    print(e)
    abort(404)


'''
PATCH /actors/<id>
'''
@app.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth('patch: actors')
def patch_actor(jwt, actor_id):
  try:
    body = request.get_json()
    actor = Actor.query.get(actor_id)
    print(body)

    if actor is None:
      abort(404)

    if "name" in body and "name" is None or "age" in body and "age" is None or "gender" in body and "gender" is None:
      abort(400)

    if "name" in body:
      actor.name = body['name']

    if "age" in body:
      actor.age = body['age']

    if "gender" in body:
      actor.gender = body['gender']

    if "cast" in body:
      movies = body['cast']

      ids = [movie['id'] for movie in movies if type(movie) is not int]
      print("old movies")
      for movie in actor.movies:
        print(movie.id)
        if movie.id not in (ids):
          delete_movie_cast(movie.id, actor_id)

      print("new movies")
      for movie in movies:
        print(movie)
        if type(movie) is int:
          add_movie_cast(movie, actor.id)
    
    actor.update()

    return jsonify({
      'success': True
    }), 200

  except Exception as e:
    print(e)
    abort(404)


'''
DELETE /actors/<id>
'''
@app.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete: actors')
def delete_actors(jwt, actor_id):
  try:
    actor = Actor.query.get(actor_id)

    if actor is None:
      abort(404)
        
    actor.delete()

    return jsonify({
      'success': True
    })
    
  except Exception:
    abort(404)


# Error Handling
'''
Error Handler for 400
'''
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': "bad request"
    }), 400


'''
Error Handler for 401
'''
@app.errorhandler(401)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': "unauthorized"
    }), 401


'''
Error Handler for 404
'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': "unprocessable"
    }), 404


'''
Error Handler for 405
'''
@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': "method not allowed"
    }), 405


'''
Error Handler for 422
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
Error Handler for 500
'''
@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': "internal server error"
    }), 500


'''
Error Handler for AuthError
'''
@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        'success': False,
        'error': error.status_code,
        'message': error.error['description']
    }), error.status_code
