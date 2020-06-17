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
MovieActor
an assosiation table, extends the base SQLAlchemy Table
'''
movieActor = db.Table("movie_actors",
    db.Column("movie_id", db.Integer, db.ForeignKey("movies.id")),
    db.Column("actor_id", db.Integer, db.ForeignKey("actors.id"))
)

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
            'release_date': self.release_date,
            'cast': [actor.format() for actor in self.cast]
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
Actor
a persistent actor entity, extends the base SQLAlchemy Model
'''
class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    name = Column(String(100), unique=True)
    age =  Column(String(3), nullable=False)
    gender =  Column(String(10), nullable=False)
    movies = db.relationship("Movie", secondary=movieActor, backref=db.backref("cast", lazy="dynamic"))

    '''
    format()
        representation of the Actor model
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
            actor = Actor(name=req_name, age=req_age, gender=req_gender)
            actor.insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            actor = Actor(name=req_name, age=req_age, gender=req_gender)
            actor.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            actor = Actor.query.filter(Actor.id == id).one_or_none()
            actor.name = 'Elijah Wood'
            actor.update()
    '''
    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())