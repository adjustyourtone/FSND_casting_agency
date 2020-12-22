import os
import unittest
import json

from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movie, Actor


# # Helper function to make testing easier
# def test_get_all_actors():
#     query = Actor.query.all()
#     return query


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
        self.casting_assistant = os.getenv("ASSISTANT_TOKEN")

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
        """Successfully test get_actors with token"""
        response = self.client().get('/api/actors', headers={"Content-Type": "application/json",
                                                             "Authorization": "Bearer {}".format(self.casting_assistant)
                                                             })
        data = json.loads(response.data)

        self.assertTrue(data['success'], True)
        self.assertEqual(response.status_code, 200)

    def test_get_all_actors_401(self):
        """Test to make sure a failed request returns HTTP Status 401"""
        response = self.client().get('/api/actors')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)


# Run Test.py
if __name__ == "__main__":
    unittest.main()
