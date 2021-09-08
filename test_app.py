import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movie, Actor
class CapstoneTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone"
        #self.database_name = "capstone_test"
        self.database_path = "postgres://postgres:pttt@{}/{}".format(
            'localhost:5432', self.database_name)
        #self.database_path = "postgres://postgres:postgres@{}/{}".format(
        #    'localhost:5432', self.database_name)    
        setup_db(self.app, self.database_path)
        self.castingdirector = "eyJhbGciOiJSUzI1Ni***"
        self.executiveproducer = "eyJhbGciOiJSUzI1***"
        self.castingassitant = "eyJhbGciOiJSUzI1N***"
        self.actor = {
            "id": 3,
            "name": "SDF",
            "age": 35,
            "gender": "Male"
        }
        self.movie = {
            "id": 3,
            "title": "My Hope in life",
            "release_date": 20090912
        }
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
    def tearDown(self):
        pass
    # GET
    def test_get_actors(self):
        res = self.client().get(
            '/actors', headers={"Authorization": "Bearer {}".format(self.executiveproducer)})
        print(res.data)
        data = json.loads(res.data)
        self.assertTrue(data['actors'])
        self.assertEqual(data['success'], True)
if __name__ == "__main__":
    unittest.main()