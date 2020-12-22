import os
import unittest
import json

from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movie, Actor


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


# Run Test.py
if __name__ == "__main__":
    unittest.main()
