import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    # user bearer tokens (needs to be udated daily):
    userTokens = {
        'executiveproducer': str(os.environ.get(['EXECUTIVE_PRODUCER_TOKEN'])),
        'castindirector': str(os.environ.get(['DIRECTOR_TOKEN'])),
        'castingassistant': str(os.environ.get(['ASSISTENT_TOKEN']))
    }

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "castingagency_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_movie = {
            'title': 'The Lord of the Rings: The Return of the King',
            'release_date': '2003-12-17T15:46:53.887+01:00'
        }

        self.false_movie = {
            'noname': 'alert=("Hello World")'
        }

        self.new_movie_as_director = {
            'title': 'Star Wars: Episode IV - A New Hope',
            'release_date': '1978-01-29T15:46:53.887+01:00'
        }

        self.new_actor = {
            'name': 'Elijah Wood',
            'age': 39,
            'gender': 'Male'
        }

        self.false_actor = {
            'noname': 'alert=("Hello World")'
        }

        self.new_actor_as_director = {
            'name': 'Sean Astin',
            'age': 49,
            'gender': 'Male'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # Correct test create_movie() request
    def test_create_movie(self):
        res = self.client().post('/movies', json=self.new_movie, headers={"Authorization": "Bearer {}".format(self.userTokens['executiveproducer'])})
        self.assertEqual(res.status_code, 200)

    # Error test create_movie() request
    def test_error_create_movie(self):
        res = self.client().post('/movies', json=self.false_movie, headers={"Authorization": "Bearer {}".format(self.userTokens['executiveproducer'])})
        self.assertEqual(res.status_code, 404)

    # Correct test create_actor() request
    def test_create_actor(self):
        res = self.client().post('/actors', json=self.new_actor, headers={"Authorization": "Bearer {}".format(self.userTokens['executiveproducer'])})
        self.assertEqual(res.status_code, 200)
    
    # Error test create_actor() request
    def test_error_create_actor(self):
        res = self.client().post('/actors', json=self.false_actor, headers={"Authorization": "Bearer {}".format(self.userTokens['executiveproducer'])})
        self.assertEqual(res.status_code, 404)
    
    # Correct test get_movies() endpoint for retrieving movies
    def test_get_movies(self):
        res = self.client().get('/movies', headers={"Authorization": "Bearer {}".format(self.userTokens['executiveproducer'])})
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json['movies'])
    
    # Error test get_movies() endpoint for retrieving movies
    def test_error_get_movies(self):
        res = self.client().get('/movies')
        self.assertEqual(res.status_code, 401)

    # Correct test get_actors() endpoint for retrieving actors
    def test_get_actors(self):
        res = self.client().get('/actors', headers={"Authorization": "Bearer {}".format(self.userTokens['executiveproducer'])})
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json['actors'])

    # Error test get_actors() endpoint for retrieving actors
    def test_error_get_actors(self):
        res = self.client().get('/actors')
        self.assertEqual(res.status_code, 401)
    
    # Correct test patch_movie(1)
    def test_patch_movie(self):
        res = self.client().patch('/movies/2', json={'title': 'edited movie'}, headers={"Authorization": "Bearer {}".format(self.userTokens['executiveproducer'])})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json['movie']['title'], "edited movie")
    
    # Error test patch_movie(1)
    def test_error_patch_movie(self):
        res = self.client().patch('/movies/20', json={}, headers={"Authorization": "Bearer {}".format(self.userTokens['executiveproducer'])})
        self.assertEqual(res.status_code, 404)
    
    # Correct test patch_actor(1)
    def test_patch_actor(self):
        res = self.client().patch('/actors/2', json={'age': 40}, headers={"Authorization": "Bearer {}".format(self.userTokens['executiveproducer'])})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json['actor']['age'], '40')
    
    # Error test patch_actor(1)
    def test_error_patch_actor(self):
        res = self.client().patch('/actors/20', json={}, headers={"Authorization": "Bearer {}".format(self.userTokens['executiveproducer'])})
        self.assertEqual(res.status_code, 404)
        
    # Correct test delete_movie(1)
    def test_delete_movie(self):
        res = self.client().delete('/movies/1', headers={"Authorization": "Bearer {}".format(self.userTokens['executiveproducer'])})
        self.assertEqual(res.status_code, 200)
    
    # Error test delete_movie(30)
    def test_error_delete_movie(self):
        res = self.client().delete('/movies/30', headers={"Authorization": "Bearer {}".format(self.userTokens['executiveproducer'])})
        self.assertEqual(res.status_code, 404)

    # Correct test delete_actor(1)
    def test_delete_actor(self):
        res = self.client().delete('/actors/1', headers={"Authorization": "Bearer {}".format(self.userTokens['executiveproducer'])})
        self.assertEqual(res.status_code, 200)

    # Error test delete_actor(90)
    def test_error_delete_actor(self):
        res = self.client().delete('/actors/90', headers={"Authorization": "Bearer {}".format(self.userTokens['executiveproducer'])})
        self.assertEqual(res.status_code, 404)

    # Casting Assistant #
    # Correct test get_movies() endpoint for retrieving movies as assistant
    def test_get_movies_as_assistant(self):
        res = self.client().get('/movies', headers={"Authorization": "Bearer {}".format(self.userTokens['castingassistant'])})
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json['movies'])

    # Correct test get_actors() endpoint for retrieving actors as assistant
    def test_get_actors_as_assistant(self):
        res = self.client().get('/actors', headers={"Authorization": "Bearer {}".format(self.userTokens['castingassistant'])})
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json['actors'])
    
    # Unauthorized test create_movie() request as assistant
    def test_create_movie_as_assistant(self):
        res = self.client().post('/movies', json=self.new_movie, headers={"Authorization": "Bearer {}".format(self.userTokens['castingassistant'])})
        self.assertEqual(res.status_code, 401)

    # Unauthorized test create_actor() request as assistant
    def test_create_actor_as_assistant(self):
        res = self.client().post('/actors', json=self.new_actor, headers={"Authorization": "Bearer {}".format(self.userTokens['castingassistant'])})
        self.assertEqual(res.status_code, 401)

    # Casting Director #
    # Correct test get_movies() endpoint for retrieving movies as director
    def test_get_movies_as_director(self):
        res = self.client().get('/movies', headers={"Authorization": "Bearer {}".format(self.userTokens['castindirector'])})
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json['movies'])

    # Correct test get_actors() endpoint for retrieving actors as director
    def test_get_actors_as_director(self):
        res = self.client().get('/actors', headers={"Authorization": "Bearer {}".format(self.userTokens['castindirector'])})
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json['actors'])
    
    # Unauthorized test create_movie() request as assistant
    def test_create_movie_as_director(self):
        res = self.client().post('/movies', json=self.new_movie_as_director, headers={"Authorization": "Bearer {}".format(self.userTokens['castindirector'])})
        self.assertEqual(res.status_code, 401)

    # Unauthorized test create_actor() request as assistant
    def test_create_actor_as_director(self):
        res = self.client().post('/actors', json=self.new_actor_as_director, headers={"Authorization": "Bearer {}".format(self.userTokens['castindirector'])})
        self.assertEqual(res.status_code, 200)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()