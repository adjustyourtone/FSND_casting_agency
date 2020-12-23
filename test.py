import os
import unittest
import json

from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movie, Actor


# Helper function to make testing easier
def test_insert_new_actor():
    insert_data = {
        'name': 'John Smith',
        'age': 32,
        'gender': 'Male'
    }
    actor = Actor(**insert_data)
    actor.insert()

    return insert_data


# Create a Test Case Class
class RolesTestCase(unittest.TestCase):
    """This class will establish the Roles test case."""

    def setUp(self):
        """Create test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'castingagency'
        self.database_path = 'postgresql://postgres:root@localhost:5432/castingagency'
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

            self.db.create_all()
        # Include JWT's for testing
        self.casting_assistant = os.getenv("ASSISTANT_TOKEN")
        self.director = os.getenv("DIRECTOR_TOKEN")
        self.producer = os.getenv("PRODUCER_TOKEN")

        self.insert_new_actor = {
            'name': 'Dixie Smith',
            'age': 32,
            'gender': 'Male'

        }

        self.insert_new_movie = {
            'title': "Dodgeball",
            'release_date': "March 3rd, 2003"
        }

        self.edit_actor = {
            'name': 'John Wayne'
        }

        self.edit_movie = {
            'id': 6,
            'title': 'Award Winning Movie'
        }

    def tearDown(self):
        """Run after each reach test."""
        pass

    def test_health_check(self):
        """Test that the application is running"""
        response = self.client().get('/')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'Healthy')

    # Get all Actors - Pass and Fail
    def test_get_all_actors(self):
        """Successfully test get_actors with assistant token"""
        response = self.client().get('/api/actors',
                                     headers={"Content-Type": "application/json",
                                              "Authorization": "Bearer {}".format(self.casting_assistant)})
        data = json.loads(response.data)

        self.assertTrue(data['success'], True)
        self.assertEqual(response.status_code, 200)

    def test_get_all_actors_401(self):
        """Test to make sure a failed request (no token) returns HTTP Status 401"""
        response = self.client().get('/api/actors')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)

    # Get all Movies - Pass and Fail

    def test_get_all_movies(self):
        """Use a Director Token to fetch all movies"""
        response = self.client().get('/api/movies',
                                     headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(self.director)})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'], True)

    def test_get_all_movies_401(self):
        """Test failure to get movies without Authorization"""
        response = self.client().get('/api/movies')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)

    # Post new actor - Pass and Fail

    # def test_post_new_actor(self):
    #     """Use a Director Token to create a new actor"""
    #     response = self.client().post('/api/actors',
    #                                   headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(self.director)}, json=self.insert_new_actor)

    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(['success'], True)

    # def test_post_new_actor_401(self):
    #     """Test failure to create an actor with assistant token"""
    #     response = self.client().post('/api/actors',
    #                                   headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(self.casting_assistant)}, json=self.insert_new_actor)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 401)

    # Post New Movie - Pass and Fail

    # def test_post_new_movie(self):
    #     """Use Producer Token to Create new movie"""
    #     response = self.client().post('/api/movies',
    #                                   headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(self.producer)}, json=self.insert_new_movie)

    #     data = json.loads(response.data)

    #     self.assertTrue(['success'], True)
    #     self.assertEqual(response.status_code, 200)

    # def test_post_new_movie_401(self):
    #     """Test failure to create movie with Director Token"""
    #     response = self.client().post('/api/movies',
    #                                   headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(self.director)}, json=self.insert_new_movie)

    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 401)

    # Edit Actor - Past and Fail
    # def test_edit_actor(self):
    #     """Use Director token to edit an actor"""
    #     response = self.client().patch('/api/actors/3',
    #                                    headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(self.director)}, json=self.edit_actor)

    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(['success'], True)

    # def test_edit_actor_401(self):
    #     """Test failure to edit actor with assistant token"""
    #     response = self.client().patch('/api/actors/1',
    #                                    headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(self.casting_assistant)}, json=self.edit_actor)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 401)

    # Edit Movie - Pass and Fail
    # def test_edit_movie(self):
    #     """Use Producer token to edit a movie."""
    #     response = self.client().patch('/api/movies/3',
    #                                    headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(self.producer)}, json=self.edit_movie)

    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(['success'], True)

    # def test_edit_movie_401(self):
    #     """Test failure to edit movie with Assistant Token"""
    #     response = self.client().patch('/api/movies/5',
    #                                    headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(self.casting_assistant)}, json=self.edit_movie)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 401)
    # Delete Actor - Pass and Fail

    # def test_delete_actor(self):
    #     """Use producer token to delete an actor"""
    #     response = self.client().delete('/api/actors/2',
    #                                     headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(self.producer)})

    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(['success'], True)

    # def test_delete_actor_401(self):
    #     """Test failure to delete an actor with assistant token."""
    #     response = self.client().delete('/api/actors/1',
    #                                     headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(self.casting_assistant)})

    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 401)

    # Delete Movie - Pass and Fail
    def test_delete_actor(self):
        """Use producer token to delete a movie."""
        response = self.client().delete('/api/movies/6',
                                        headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(self.producer)})

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(['success'], True)

    def test_delete_actor_401(self):
        """Test failure to delete an actor with a Director token."""
        response = self.client().delete('/api/movies/5',
                                        headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(self.director)})

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)


# Run Test.py
if __name__ == "__main__":
    unittest.main()
