import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth

def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)
    return app
app = create_app()
db = setup_db(app)

@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Headers'] = 'Authorization, Content-Type, true'
    header['Access-Control-Allow-Methods'] = 'POST,GET,PUT,DELETE,PATCH,OPTIONS'
    return response

@app.route('/')
def homepage():
    return jsonify({
        "success": 200
    })

@app.route("/movies")
@requires_auth("get:movies")
def get_movies(token):
    try:
        movies = Movie.query.all()
        movies = [movie.format() for movie in movies]
        return jsonify({
            'success': True,
            'movies': movies
        })
    except:
        abort(422)

@app.route("/actors")
@requires_auth("get:actors")
def get_actors(token):
    try:
        actors = Actor.query.all()
        actors = [actor.format() for actor in actors]
        return jsonify({
            'success': True,
            'actors': actors
        })
    except:
        abort(422)

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad request"
    }), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource not found"
    }), 404

@app.errorhandler(405)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "Method not allowed"
    }), 404

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable"
    }), 422

@app.errorhandler(500)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal Server Error"
    }), 500

@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify(error.error), error.status_code
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)