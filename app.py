import os
from flask import Flask, request, abort, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth
from sqlalchemy import exc
import json

AUTH0_CALLBACK_URL = os.getenv('AUTH0_CALLBACK_URL')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_BASE_URL = os.getenv('AUTH0_BASE_URL')
AUTH0_AUDIENCE = os.getenv('AUTH0_AUDIENCE')


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PATCH, PUT, POST, DELETE, OPTIONS')
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response

    # auxiliary endpoint to get token

    @app.route('/authorization/url', methods=['GET'])
    def generate_auth_url():
        url = f'https://{AUTH0_DOMAIN}/authorize' \
            f'?audience={AUTH0_AUDIENCE}' \
            f'&response_type=token&client_id=' \
            f'{AUTH0_CLIENT_ID}&redirect_uri=' \
            f'{AUTH0_CALLBACK_URL}'

        return jsonify({
            'url': url
        })

    @app.route('/')
    def homepage():
        return jsonify({
            "success": 200
        })

    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(token):
        try:
            actors = Actor.query.all()
            formated_actors = {}
            for actor in actors:
                formated_actors[actor.id] = actor.format()
            return jsonify({
                'success': True,
                'actors': formated_actors
            })
        except BaseException:
            return jsonify({
                "success": False,
                "error": 500,
                "message": "internal server error"
            }), 500

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(token):
        try:
            movies = Movie.query.all()
            formated_movies = {}
            for movie in movies:
                formated_movies[movie.id] = movie.format()
            return jsonify({
                'success': True,
                'movies': formated_movies
            })
        except BaseException:
            return jsonify({
                "success": False,
                "error": 500,
                "message": "internal server error"
            }), 500

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(token, actor_id):
        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            if not actor:
                return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                }), 404

            actor.delete()
            actors = Actor.query.all()
            formated_actors = {}
            for actor in actors:
                formated_actors[actor.id] = actor.format()
            return jsonify({
                'success': True,
                'deleted': actor_id
                # 'actors': formated_actors
            })
        except BaseException as err:
            print('Handling run-time error : ', err)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(token, movie_id):
        try:
            movie = Movie.query.filter(
                Movie.id == movie_id
            ).one_or_none()
            if not movie:
                return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                }), 404

            movie.delete()
            formated_movies = {}
            movies = Movie.query.all()
            for movie in movies:
                formated_movies[movie.id] = movie.format()
                return jsonify({
                    'success': True,
                    'deleted': movie_id
                    # 'movies': formated_movies
                })
        except BaseException as err:
            print("Handle error : ", err)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(token):

        body = request.get_json()
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
        movie_id = body.get('movie_id', None)

        if name == '' or age == '' or gender == '' or movie_id == '':
            return jsonify({
                "success": False,
                "error": 422,
                "message": "unprocessable"
            }), 422
        try:
            actor = Actor(name=name, age=age, gender=gender, movie_id=movie_id)
            actor.insert()
            actors = Actor.query.all()
            formated_actors = {}
            for actor in actors:
                formated_actors[actor.id] = actor.format()
            return jsonify({
                'success': True,
                'actors': formated_actors
            })
        except BaseException:
            return jsonify({
                "success": False,
                "error": 500,
                "message": "internal server error"
            }), 500

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(token):
        try:
            body = request.get_json()
            title = body.get('title', None)
            release_date = body.get('release_date', None)
            if title == '' or release_date == '':
                return jsonify({
                    "success": False,
                    "error": 422,
                    "message": "unprocessable"
                }), 422
            movie = Movie(title=title, release_date=release_date)
            movie.insert()
            formated_movies = {}
            movies = Movie.query.all()
            for movie in movies:
                formated_movies[movie.id] = movie.format()
            return jsonify({
                'success': True,
                'movies': formated_movies
            })
        except BaseException:
            return jsonify({
                "success": False,
                "error": 500,
                "message": "internal server error"
            }), 500

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actor')
    def update_actor(token, actor_id):
        try:
            actor = Actor.query.filter(
                Actor.id == actor_id
            ).one_or_none()
            if actor is None:
                return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                }), 404

            body = request.get_json()
            name = body.get('name', None)
            age = body.get('age', None)
            gender = body.get('gender', None)
            movie_id = body.get('movie_id', None)

            actor.name = name
            actor.age = age
            actor.gender = gender
            actor.movie_id = movie_id

            actor.update()

            actors = Actor.query.all()
            formated_actors = {}
            for actor in actors:
                formated_actors[actor.id] = actor.format()
            return jsonify({
                'success': True,
                'actors': formated_actors
            })
        except BaseException:
            return jsonify({
                "success": False,
                "error": 500,
                "message": "internal server error ///"
            }), 500

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movie')
    def update_movie(token, movie_id):
        try:
            movie = Movie.query.filter(
                Movie.id == movie_id
            ).one_or_none()
            if movie is None:
                return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                }), 404

            body = request.get_json()
            title = body.get('title', None)
            release_date = body.get('release_date', None)
            movie.title = title
            movie.release_date = release_date
            movie.update()
            formated_movies = {}
            movies = Movie.query.all()
            for movie in movies:
                formated_movies[movie.id] = movie.format()
            return jsonify({
                'success': True,
                'movies': formated_movies

            })
        except BaseException:
            return jsonify({
                "success": False,
                "error": 500,
                "message": "internal server error"
            }), 500

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": 'unauthorized'
        }), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": 'method not allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    @app.errorhandler(AuthError)
    def handle_auth_error(error):

        response = jsonify(error.error)
        response.status_code = error.status_code

        return response

    return app


app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
