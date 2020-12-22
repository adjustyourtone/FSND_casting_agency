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

    def test_get_all_actors(self):
        """Successfully test get_actors with assistant token"""
        response = self.client().get('/api/actors', headers={"Content-Type": "application/json",
                                                             "Authorization": "Bearer {}".format(self.casting_assistant)
                                                             })
        data = json.loads(response.data)

        self.assertTrue(data['success'], True)
        self.assertEqual(response.status_code, 200)

    def test_get_all_actors_401(self):
        """Test to make sure a failed request (no token) returns HTTP Status 401"""
        response = self.client().get('/api/actors')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)

    def test_get_all_movies(self):
        """Use a Director Token to fetch all movies"""
        response = self.client().get('/api/movies',
                                     headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(self.director)})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'], True)

    def test_get_all_movies_401(self):
        """Use a Director Token to fetch all movies"""
        response = self.client().get('/api/movies')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)

    def test_post_new_actor(self):
        """Use a Director Token to create a new actor"""
        response = self.client().post('/api/actors',
                                      headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(self.director)}, json=self.insert_new_actor)

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(['success'], True)

    def test_delete_actor(self):
        """Use producer token to delete an actor"""
        response = self.client().delete('/api/actors/7',
                                        headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(self.producer)})

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(['success'], True)

    def test_delete_actor_401(self):
        """Use assistant token to delete an actor"""
        response = self.client().delete('/api/actors/7',
                                        headers={"Content-Type": "application/json", "Authorization": "Bearer {}".format(self.casting_assistant)})

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)


# Run Test.py
if __name__ == "__main__":
    unittest.main()
