import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
import json
from flask import jsonify

database_path = os.environ.get('DATABASE_URL')
if not database_path:
    database_name = "capstone"
    database_path = "postgresql://{}/{}".format('postgres:pttt@localhost:5432', database_name)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    moment = Moment(app)
    migrate = Migrate(app, db)
    with app.app_context():
        db.create_all()


class Actor(db.Model):
    __tablename__ = 'actor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(120))
    movies = db.relationship(
        'Movie',
        secondary='Show'
    )

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movies': [movie.format() for movie in self.movies]
        }


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, default=datetime.utcnow)
    actors = db.relationship(
        'Actor',
        secondary='Show'
    )

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'actors': self.actors
        }


class Show(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey(Actor.id))
    movie_id = db.Column(db.Integer, db.ForeignKey(Movie.id))
    actor = db.relationship(Actor, backref=db.backref("actor_assoc"))
    movie = db.relationship(Movie, backref=db.backref("movie_assoc"))
