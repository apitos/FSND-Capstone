from datetime import datetime
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
        self.database_path = "postgresql://postgres:password@{}/{}".format(
            'localhost:5432', self.database_name)
        
        setup_db(self.app, self.database_path)   
        
        self.Casting_Assistant = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjU5UXRqNFlFTVF3UkUydzJyVVBCRCJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWFwcC5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzM2EzMDI0ZmI1OTgwMDY5ZDBhYzc4IiwiYXVkIjoiQ2Fwc3RvbmUiLCJpYXQiOjE2MzEzNjI4NzQsImV4cCI6MTYzMTQ0OTI3NCwiYXpwIjoiSjU1VlBueXRBTGZqUHFqcldkaFdSR3Y3dlZoUlpIMFIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.tSWqDKjx8KjN1n4m1ESs0prPyeXu93WKQ7msNfjEhKdP_bNWiB_ojngFtkIm1RnAcLHPxpHHDyFH5-ok0u9yF0YWHSf2iP5JiVGnQskZEo9mKynlEAY8zLn7gFxSIzVN9w7ZWOrP0a5fElk8XaNLTkG8sXDjUPUaVKCzuRQSUP3Y06LapC5BjAsL_HUTnT3EYDrqzZYX6M_yurxvItmh76KIo5R9yo2CYl7xnnx2DoixBpq0Aiwp_beu7Z2fxOInIoq8Xt9Ow3_1ScHkbCtBpnwAaXJ1wkwD4ITbNCLGhTJCa3lc_aIaXAmYZjQSAKge0KBIsJrSTfvZ4qL6CBiU6g"
        self.Casting_Director = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjU5UXRqNFlFTVF3UkUydzJyVVBCRCJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWFwcC5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzM2EzNjlmZmQ5ZTEwMDcwMzVlNjNiIiwiYXVkIjoiQ2Fwc3RvbmUiLCJpYXQiOjE2MzEzNjI5MzMsImV4cCI6MTYzMTQ0OTMzMywiYXpwIjoiSjU1VlBueXRBTGZqUHFqcldkaFdSR3Y3dlZoUlpIMFIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTphY3Rvcl9mcm9tX21vdmllIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvcnMiLCJwb3N0OmFjdG9yX3RvX21vdmllIl19.lVnsKEwo9okIB1XI0lSDlGOeXoIR3A5YIgKGmJJZGaK-cK78t8oktT8yxHGiyfDkoXHltupRwoiSfDlO3IgHmVfhxL4xrgRKtj73NdY11q9T7jnH9FPKwbL9vsb7G-IU-EP6rF1FTohV8OijqaU4AHCMW4Unl5nR2fvb9hO0pjW1vnV3WFhOxU0THp3KajejS5Sds-yaWMPkMpSiZx1Viyu6iNKXWKffveMYaBhXjnfQcSvOy55U4Ewq7c84BOb_kMfRPyyxPyVt6UCetQ90_zcs6funuYKy3JhDZzH0KhcMSY1wuWmiC5NhDkkttSnn8lnbNYzu5_Gs-pdXyka1vg"
        self.Executive_Producer = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjU5UXRqNFlFTVF3UkUydzJyVVBCRCJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWFwcC5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzM2EzYTgxZWU0YjYwMDY5NDA3ZDQzIiwiYXVkIjoiQ2Fwc3RvbmUiLCJpYXQiOjE2MzEzNjIwNTgsImV4cCI6MTYzMTQ0ODQ1OCwiYXpwIjoiSjU1VlBueXRBTGZqUHFqcldkaFdSR3Y3dlZoUlpIMFIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.bboT0nnG2bH9KH0wohPFxo2ZlNIuS_K9nl9JzbC1oUY4fcMjIRiMTrLPrMavJhMQrYnBnYpSPf_zTyaMW4CO2QwrjgfI-VEoK-98vZr_smqZGDk-Gr3lhJ0HND-3RxBXNNNeI-iHpqdbF9mgcimbYZ35OCHp1HdKi2lfGJO1ahXh08E9rafhbaZSe97DNqs5XP6MfPIExJk7BPxtYOJrXqq_Vpn-7yLUK4oS4CLZRsKy2ogbqOuQZoky8Uzf6t2ppEGwnpguP56idf697Gkw_DBtAJHsfG-2YbeeS5ckMHrdWLri5vLC9msfSGjQcwX7_L0ZvMEhxfiHXbRuVCFqHQ"

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
            '/actors', headers={"Authorization": "Bearer {}".format(self.Casting_Assistant)})    
        
        data = json.loads(res.data)
        
        self.assertTrue(data['actors'])
        self.assertEqual(data['success'], True)
        

    def test_get_actors_as_casting_assistant(self):

        response = self.client().get('/actors', headers={
            'Authorization': 'Bearer ' + self.Casting_Assistant})
        self.assertEqual(response.status_code, 200)

    def test_get_actors_as_casting_director(self):
        response = self.client().get('/actors', headers={
            'Authorization': 'Bearer ' + self.Casting_Director})
        self.assertEqual(response.status_code, 200)

    def test_post_actor_as_casting_director(self):
        
        response = self.client().post('/actors', headers={
            'Authorization': 'Bearer ' + self.Casting_Director},
            json={
                "name": "Anthony",
                "age": 72,
                "gender": "Male",
                "movie_id": 1
                })

        self.assertEqual(response.status_code, 200)

        
    def test_delete_actor_as_casting_assistant(self):
        response = self.client().delete('/actors/1', headers={
            'Authorization': 'Bearer ' + self.Casting_Assistant})

        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')


    def test_post_movie_as_casting_director(self):
        response = self.client().post('/movies', headers={
           'Authorization': 'Bearer ' + self.Casting_Director},
           json={
                "title": "Dumb and Dumber",
                "release_date": "1985",
                })

        data = json.loads(response.data)
                    
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    
    def test_post_movie_as_executive_producer(self):
        response = self.client().post('/movies', headers={
            'Authorization': 'Bearer ' + self.Executive_Producer},
            json={
                "title": "March of the Penguins",
                "release_date": "2010",
                })

        self.assertEqual(response.status_code, 200)


    def test_get_movies_as_casting_assistant(self):
        response = self.client().get('/movies', headers={
            'Authorization': 'Bearer ' + self.Casting_Assistant})
        self.assertEqual(response.status_code, 200)


    def test_get_movies_as_executive_producer(self):
        response = self.client().get('/movies', headers={
            'Authorization': 'Bearer ' + self.Executive_Producer})
        self.assertEqual(response.status_code, 200)


    
    def test_delete_movie_as_casting_assistant(self):
        response = self.client().delete('/movies/1', headers={
            'Authorization': 'Bearer ' + self.Casting_Assistant})
        data = json.loads(response.data)
    
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    
    def test_patch_actor_as_casting_director(self):
        response = self.client().patch('/actors/3', headers={
            'Authorization': 'Bearer ' + self.Casting_Director},
            json={
                "name": "Patrick",
                "age": 18,
                "gender": "Male",
                "movie_id": 2
                })

        self.assertEqual(response.status_code, 200)

    def test_patch_movie_as_casting_assistant(self):
        response = self.client().patch('/movies/1', headers={
            'Authorization': 'Bearer ' + self.Casting_Assistant},
            json={
                "title": "Impress Your Friends With a Well-Trained Human!",
                "release_date": "2021"
                })

        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')


if __name__ == "__main__":
    unittest.main()