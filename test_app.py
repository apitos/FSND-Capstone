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

        self.Casting_Assistant = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjU5UXRqNFlFTVF3UkUydzJyVVBCRCJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWFwcC5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzM2EzMDI0ZmI1OTgwMDY5ZDBhYzc4IiwiYXVkIjoiQ2Fwc3RvbmUiLCJpYXQiOjE2MzE1NjIwMDgsImV4cCI6MTYzMTY0ODQwOCwiYXpwIjoiSjU1VlBueXRBTGZqUHFqcldkaFdSR3Y3dlZoUlpIMFIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.PRUWq9gu8zfKibc_GJ71ZNfok4HMd7Ppdq0AmHtNhVfWG_dNHnBSlPOkq8uCd22mumV5hP7kss0irIlDcZCwlxxEHBvoYBweLmhTW-guK_dCbavBuoJ7lh4mssUAmP1WfRhf66mg5TYY9FwKK_yZKIJlmbt4JlDIjfuOuTj-1qk6b3cg2EFDZyoOqLjaABGIfSv8vb01dW4ZEN7l_5Nyc7uS81XsamZC0UcfubMk5f277fK8A-HZ4xVl0hgTWI9-iq-KsgOMrAVL-0ZPeccekb-YdKRLR_CON0EZgzooi7fK7a8p1JAvWn5205nIHJ1IOln-VG7y94obW3eljhLKJw"
        self.Casting_Director = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjU5UXRqNFlFTVF3UkUydzJyVVBCRCJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWFwcC5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzM2EzNjlmZmQ5ZTEwMDcwMzVlNjNiIiwiYXVkIjoiQ2Fwc3RvbmUiLCJpYXQiOjE2MzE1NjQ2MTEsImV4cCI6MTYzMTY1MTAxMSwiYXpwIjoiSjU1VlBueXRBTGZqUHFqcldkaFdSR3Y3dlZoUlpIMFIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTphY3Rvcl9mcm9tX21vdmllIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvcnMiLCJwb3N0OmFjdG9yX3RvX21vdmllIl19.Zczq4_qzxViaTh6GlyeUarMksefMkjKNitOkLmoPYZ-tl9DKT-zpYUnVduOVCgLbAQgZI_1K1_2GNPFJfv7Wjf0TgTeOA1K5yd13pzaWGqSQYq3SSBI1-kmO6gBKIfGG3hPc2I4OTTrjt2Q5a7gxKYvVWG9wERw-PJutjghTKAJcsTp8gwOaBRLNRe0v9rywNyHCHnxupxbkBKdv5kVUW7jUzme8MZWVgLZ2oQrsaTh4rXOUI12By78GZbRphOQzygJZ8kzaFfOhDzuucuvMrpX1RFcdTgXXFJt1Pgn6NJN1o9-A4WyH38ZtVyeKiPNOHLdUkYInnv3K6Vb825LtWw"
        self.Executive_Producer = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjU5UXRqNFlFTVF3UkUydzJyVVBCRCJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWFwcC5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzM2EzYTgxZWU0YjYwMDY5NDA3ZDQzIiwiYXVkIjoiQ2Fwc3RvbmUiLCJpYXQiOjE2MzE1NjQ3MDgsImV4cCI6MTYzMTY1MTEwOCwiYXpwIjoiSjU1VlBueXRBTGZqUHFqcldkaFdSR3Y3dlZoUlpIMFIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.sGA7sNPETSdNQF04YpJR7E2OZw5IbPu1tLqBt7HUEyUFDmszbIutSOslnpVP_KoDVTT0qogSJwQjsar70EpzrjdBWhcZLsXOdVc4Oc0O4eh-XUEeqFUpDQpf_Zlc-uBzkKStbDD0u_gezitnk6cJ_2g_VqycSTi2MZ5sb4YdTmIEPyDBAcNj8PBMM1uNlp3mL1TQREXLSNdV6moBhYzPkLXSUJeV_qrFQKHwgl0WonO3y95B9GnfhRcqiI-RIiUlRHKJTJtbADZ87bQMlHhlbB1iBoEVIJ3CW2Qj-KWc8z6_nUUWONLS9VChnLjrgciSE7aDC_zsItyeIh-7EyQtlw"

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
            '/actors',
            headers={
                "Authorization": "Bearer {}".format(
                    self.Casting_Assistant)})

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
                "title": "The independance day",
                "release_date": "2018"
        })

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')


if __name__ == "__main__":
    unittest.main()
