import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Movie, Actor
from auth.auth import AUTH0_DOMAIN, CLIENT_ID, REDIRECT_URL, LOGOUT_URL, \
    API_AUDIENCE, AuthError, requires_auth
from flask_migrate import Migrate


# db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__)
    # migrate = Migrate(app, db)
    setup_db(app)
    CORS(app, resources={r"/api/*"})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE')
        return response

# ----------------------------------------------------------#
# Routes
# ----------------------------------------------------------#
    @app.route('/')
    def health_check():
        return jsonify({
            'status': 'Healthy'
        }), 200

    # This endpoint will allow you to sign in to Auth0 to generate a new
    # access token. Please read the section on Token Generation in the
    # README.MD
    @app.route("/authorization/url", methods=["GET"])
    def generate_auth_url():
        """This endpoint will allow you to generate an auth URL."""
        url = f'https://{AUTH0_DOMAIN}/authorize' \
            f'?audience={API_AUDIENCE}' \
            f'&response_type=token&client_id=' \
            f'{CLIENT_ID}&redirect_uri=' \
            f'{REDIRECT_URL}'
        return jsonify({
            'message': 'Click this link to sign in.',
            'url': url
        }), 200

    # NOTE: Use this endpoint to easily logout of an Auth0 session to generate
    # a new access token. See README.MD for more information.
    @app.route('/authorization/logout', methods=['GET'])
    def generate_logout_url():
        """This endpoint will clear your Auth0 session."""
        url = f'https://{AUTH0_DOMAIN}/v2/logout?federated&' \
            f'client_id={CLIENT_ID}&returnTo={LOGOUT_URL}'

        return jsonify({
            'message': 'Click this link to logout of your Auth0 session.',
            'logout_url': url
        }), 200

    @app.route('/logout')
    def logout():
        return f"<html><body><p>You are logged out and will be redirected\
             momentarily.</p><script>var timer = setTimeout(function()\
                  {{window.location='{ '/authorization/url' }'}}, 3000);\
                      </script></body></html>"

    @app.route('/api/actors')
    @requires_auth('get:actors')
    def get_actors(payload):
        """This endpoint will retrieve all actors."""
        try:
            actors = Actor.query.all()

            return jsonify({
                'success': True,
                'actors': [actor.format() for actor in actors]
            }), 200
        except BaseException:
            abort(401)

    @app.route('/api/movies')
    @requires_auth('get:movies')
    def get_movies(payload):
        """This endpoint will retrieve all movies."""
        try:
            movies = Movie.query.all()

            return jsonify({
                'success': True,
                'movies': [movie.format() for movie in movies]
            })
        except BaseException:
            abort(401)

    @app.route('/api/actors/<int:id>', methods=['GET'])
    @requires_auth('get:actors')
    def view_actor(payload, id):
        """This endpoint will show an actor by ID"""
        actor = Actor.query.get(id)

        return jsonify({
            'success': True,
            'actor': actor.format()
        })

    @app.route('/api/movies/<int:id>', methods=['GET'])
    @requires_auth('get:movies')
    def view_movie(payload, id):
        """This endpoint will show a movie by ID"""
        movie = Movie.query.get(id)

        return jsonify({
            'success': True,
            'movie': movie.format()
        })

    @app.route('/api/actors', methods=['POST'])
    @requires_auth('post:actor')
    def create_actor(payload):
        """This endpoint will allow the creation of a new actor."""
        data = request.get_json()

        try:
            new_actor = Actor()
            new_actor.name = data['name']
            new_actor.age = data['age']
            new_actor.gender = data['gender']

            new_actor.insert()

        except BaseException:
            abort(400)

        return jsonify({
            'success': True,
            'actor': new_actor.format()
        }), 200

    @app.route('/api/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actor')
    def update_actor(payload, id):
        """This endpoint will allow one to edit an actor"""
        actor = Actor.query.get(id)

        if actor is None:
            abort(404)

        data = request.get_json()

        if 'name' in data:
            actor.name = data['name']
        if 'age' in data:
            actor.age = data['age']
        if 'gender' in data:
            actor.gender = data['gender']

        actor.update()

        return jsonify({
            'success': True,
            'actor': actor.format()
        }), 200

    @app.route('/api/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(payload, id):

        try:
            actor = Actor.query.get(id)

            if actor is None:
                abort(404)

            actor.delete()

            return jsonify({
                'success': True,
                'delete': actor.format()
            }), 200

        except BaseException:
            abort(401)

    @app.route('/api/movies', methods=['POST'])
    @requires_auth('post:movie')
    def create_movies(payload):
        """This endpoint will allow the creation of a new movie."""
        data = request.get_json()

        try:
            new_movie = Movie()
            new_movie.title = data['title']
            new_movie.release_date = data['release_date']

            new_movie.insert()

            return jsonify({
                'success': True,
                "movie": new_movie.format()
            }), 200

        except BaseException:
            abort(401)

    @app.route('/api/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movie')
    def update_movies(payload, id):
        """This endpoint will allow one to edit a movie by ID."""
        movie = Movie.query.get(id)

        if movie is None:
            abort(404)

        data = request.get_json()

        if 'title' in data:
            movie.title = data['title']
        if 'release_date' in data:
            movie.release_date = data['release_date']

        movie.update()

        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 200

    @app.route('/api/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(payload, id):
        """This endpoint will allow you to delete a movie by ID"""
        movie = Movie.query.get(id)

        movie.delete()

        return jsonify({
            'success': True,
            'deleted': movie.format()
        }), 200

    # Error Handlers
    @app.errorhandler(AuthError)
    def process_AuthError(error):
        """AuthError effor handler."""
        response = jsonify(error.error)
        response.status_code = error.status_code

        return response

    @app.errorhandler(400)
    def bad_request(error):
        """Bad request error handler."""
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request. Please verify the information you \
                submitted is correct and try again."
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        """Unauthorized attempt error handler."""
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized attempt."
        }), 401

    @app.errorhandler(404)
    def resource_not_found(error):
        """Resource not found error handler."""
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'This resoure has not been found.'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        """Unprocessable entity error handeler."""
        return jsonify({
            "success": False,
            "error": 422,
            "message": "This is an unprocessable entity."
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        """Internal server error error handler."""
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal server error. Please try again."
        }), 500

    return app


app = create_app()


if __name__ == '__main__':
    app.run()
