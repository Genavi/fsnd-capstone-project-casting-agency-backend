import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "capstone_casting_agency"
database_path = "postgres://{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple verisons of a database
'''
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

'''
Movie
a persistent movie entity, extends the base SQLAlchemy Model
'''
class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    title = Column(String(100), unique=True)
    release_date =  Column(String(100), nullable=False)

    '''
    format()
        representation of the Movie model
    '''
    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            movie = Movie(title=req_title, release_date=req_release_date)
            movie.insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            movie = Movie(title=req_title, release_date=req_release_date)
            movie.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            movie.title = 'The Lord of the Rings: The Fellowship of the Ring'
            movie.update()
    '''
    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())


'''
Artist
a persistent artist entity, extends the base SQLAlchemy Model
'''
class Artist(db.Model):
    __tablename__ = 'artists'

    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    name = Column(String(100), unique=True)
    age =  Column(String(3), nullable=False)
    gender =  Column(String(10), nullable=False)

    '''
    format()
        representation of the Artist model
    '''
    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            artist = Artist(name=req_name, age=req_age, gender=req_gender)
            artist.insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            artist = Artist(name=req_name, age=req_age, gender=req_gender)
            artist.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            artist = Artist.query.filter(Artist.id == id).one_or_none()
            artist.name = 'Elijah Wood'
            artist.update()
    '''
    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())


class MovieToArtist(db.Model):
    __tablename__ = 'movies_to_artists'

    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey(Movie.id, ondelete='CASCADE'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey(Artist.id, ondelete='CASCADE'), nullable=False)
        
    '''
    format()
        representation of the MovieToArtist model
    '''
    def format(self):
        return {
            'id': self.id,
            'movie_id': self.movie_id,
            'artist_id': self.artist_id
        }

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            movietoartist = MovieToArtist(movie_id=req_movie_id, artist_id=req_artist_id)
            movietoartist.insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            movietoartist = MovieToArtist(movie_id=req_movie_id, artist_id=req_artist_id)
            movietoartist.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            movietoartist = MovieToArtist.query.filter(MovieToArtist.id == id).one_or_none()
            movietoartist.movie_id = 2
            movietoartist.update()
    '''
    def update(self):
        db.session.commit()

    def __repr__(self):