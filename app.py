import os
from flask import Flask, request, abort, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from models import setup_db, Movie, Actor

from auth import AuthError, requires_auth
from sqlalchemy import exc
import json

from authlib.integrations.flask_client import OAuth

AUTH0_CALLBACK_URL = os.getenv('AUTH0_CALLBACK_URL')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_BASE_URL = os.getenv('AUTH0_BASE_URL')
AUTH0_AUDIENCE = os.getenv('AUTH0_AUDIENCE')

def create_app(test_config=None):
    # app = Flask(__name__)
    # CORS(app)
    # #return app
    # app = create_app()
    # db = setup_db(app)

    app = Flask(__name__)
    setup_db(app)
    
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    CORS(app)
# 
# auth0 info
    # oauth = OAuth(app)
    # oauth.init_app(app)

    # auth0 = oauth.register(
    #     'auth0',
    #     client_id=AUTH0_CLIENT_ID,
    #     client_secret=AUTH0_CLIENT_SECRET,
    #     api_base_url=AUTH0_BASE_URL,
    #     access_token_url='https://capstone-app.eu.auth0.com' + '/oauth/token',
    #     authorize_url='https://capstone-app.eu.auth0.com' + '/authorize',
    #     client_kwargs={
    #         'scope': 'openid profile email'
    #         }
    #     )
    # print (auth0)

    
    # @app.after_request
    # def after_request(response):
    #     header = response.headers
    #     header['Access-Control-Allow-Origin'] = '*'
    #     header['Access-Control-Allow-Headers'] = 'Authorization, Content-Type, true'
    #     header['Access-Control-Allow-Methods'] = 'POST,GET,PUT,DELETE,PATCH,OPTIONS'
    #     return response


    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                         'GET, PATCH, PUT, POST, DELETE, OPTIONS')
        response.headers.add('Access-Control-Allow-Origin', '*')
        
        return response
    

    # db_drop_and_create_all()
    # this only for initial table creation on initialization.


    @app.route('/')
    def homepage():
        return jsonify({
            "success": 200
        })

        #return redirect('https://capstone-app.eu.auth0.com/authorize?response_type=token&client_id=J55VPnytALfjPqjrWdhWRGv7vVhRZH0R&redirect_uri=https://capstone-castingag-app.herokuapp.com//movies')
        #return redirect('https://capstone-app.eu.auth0.com/authorize?response_type=token&client_id=J55VPnytALfjPqjrWdhWRGv7vVhRZH0R&redirect_uri=http://localhost:5000')


    @app.route('/actors')
    @requires_auth('get:actors')
    #def get_actors(token):
    def get_actors(payload):
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
    def get_movies(payload):
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
    def delete_actor(actor_id):

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
            'actors': formated_actors
        })

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(movie_id):

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
            'movies': formated_movies
        })

    @app.route('/actors', methods=['POST'])
    @requires_auth('add:actor')
    def create_actor():

        body = request.get_json()
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
        if name == '' or age == '' or gender == '':
            return jsonify({
                "success": False,
                "error": 422,
                "message": "unprocessable"
            }), 422
        try:
            actor = Actor(name=name, age=age, gender=gender)
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
    @requires_auth('add:movie')
    def create_movie():
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
    @requires_auth('patch:actor ')
    def update_actor(actor_id):
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
            actor.name = name
            actor.age = age
            actor.gender = gender
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
                "message": "internal server error"
            }), 500

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movie')
    def update_movie(movie_id):
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

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
            }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
            }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
            }), 400

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