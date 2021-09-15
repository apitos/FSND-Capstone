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
    database_path = "postgresql://{}/{}".format(
        'postgres:password@localhost:5432', database_name)

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


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.String(30), nullable=False)

    actors = db.relationship(
        "Actor", backref="Movie", lazy=True, cascade="all, delete-orphan"
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
            'actors': [actor.format() for actor in self.actors]
        }


class Actor(db.Model):
    __tablename__ = 'actor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(120))
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)

    def __init__(self, name, age, gender, movie_id):
        self.name = name
        self.age = age
        self.gender = gender
        self.movie_id = movie_id

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
            'movie_id': self.movie_id
        }

    def db_drop_and_create_all():
        db.drop_all()
        db.create_all()
        # add one demo row in each table which is helping in POSTMAN test
        movie = Movie(
            title="First",
            release_date="2021"
        )

        actor = Actor(
            name="I",
            age="55",
            gender="Male",
            movie_id=1
        )

        db.session.add(movie)
        db.session.add(actor)
        db.session.commit()
