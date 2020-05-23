import unittest
import json
import models
from app import create_app
from flask_sqlalchemy import SQLAlchemy
from models import db_drop_and_create_all
from models import setup_db
import pdb


class Tests (unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client
        setup_db(self.app)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
            

        pdb.set_trace()
        self.director = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkpDUFB4bUYzOWFhWTAyNUt2aWlrQSJ9.eyJpc3MiOiJodHRwczovL2Rldi15MjV3ZTU0aS5ldS5hdXRoMC5jb20vIiwic3ViIjoiMTJRVzhocFBkQnpsdEZ6OWFhU3kwVWQ5WENtcFRqMGJAY2xpZW50cyIsImF1ZCI6IlppQ2Fwc3RvbmUiLCJpYXQiOjE1OTAyMTE4NDAsImV4cCI6MTU5MDI5ODI0MCwiYXpwIjoiMTJRVzhocFBkQnpsdEZ6OWFhU3kwVWQ5WENtcFRqMGIiLCJzY29wZSI6ImdldDptb3ZpZXMgZ2V0OmFjdG9ycyBwb3N0Om1vdmllcyBwb3N0OmFjdG9ycyBwYXRjaDptb3ZpZXMgcGF0Y2g6YWN0b3JzIGRlbGV0ZTptb3ZpZXMgZGVsZXRlOmFjdG9ycyIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsInBlcm1pc3Npb25zIjpbImdldDptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwicG9zdDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBhdGNoOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJkZWxldGU6YWN0b3JzIl19.AxF0rUYLvWBHmPbJF4uJEUe1p1Aol3HfxKR3DC74ukxMlRV3Iy7UmWVQSjNNBDbVNbYVKk2pfS3Cw7tQQuUP6eBMjrVIMsuLYXNeD4FpXmMN2ROhsrR3EO6_kYzH6or2LWXsT6jryJcDZOQIKeoizfI4FGGqA2_vlg70rHi1_IgdMltqZN7Be4sH7VH17JS4Wp5NtQTBG6n9n1kBMvwzC32HXR91rBDzs5_GSedISQjfp-e_5oPT6W9uvkIaTcx1bFN_B1_B2LgAUwiiuJYpUDjWAj_8pipuEthJYRM1sNvd5g2VPY61wNVBtqJWpRyZPNylIZfDBsxe_VMUxyYu4A'

        self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer '+ self.director}

        self.newMovie = {
            'title': 'Movie 1',
            'movie_date': '2020-01-01T00:00:00'
        }
        self.newActor = {
            'name': 'Actor 1',
            'age': 22,
            'gender': 'Unkown'
        }
        self.otherMovie = {
            'title': 'Movie 1',
            'movie_date': '2020-01-01T00:00:00',
            'actors': self.newActor
        }
        self.otherActor = {
            'name': 'Actor 1',
            'age': 23,
            'gender': 'Still Unkown'
        }
        pass

    def tearDown(self):
        pass

    def testGET(self):
        res = self.client().get('/movies')
        self.assertEqual(res.status_code, 401)

        res = self.client().get(
            '/movies',
            headers=self.headers)
        self.assertEqual(res.status_code, 200)

        res = self.client().get('/actors')
        self.assertEqual(res.status_code, 401)

        res = self.client().get(
            '/actors',
            headers=self.headers)
        self.assertEqual(res.status_code, 200)

    def testPOST(self):
        res = self.client().post('/movies', json=self.newMovie)
        self.assertEqual(res.status_code, 401)

        res = self.client().post('/actors', json=self.newActor)
        self.assertEqual(res.status_code, 401)

        res = self.client().post(
            '/movies',
            headers=self.headers,
            json=self.newMovie)
        self.assertEqual(res.status_code, 200)

        res = self.client().post(
            '/actors',
            headers=self.headers,
            json=self.newActor)
        self.assertEqual(res.status_code, 200)

    def testPATCH(self):
        res = self.client().patch('/movies/1', json=self.otherMovie)
        self.assertEqual(res.status_code, 401)

        res = self.client().patch('/actors/1', json=self.otherActor)
        self.assertEqual(res.status_code, 401)

        res = self.client().patch(
            '/movies/1',
            headers=self.headers,
            json=self.otherMovie)
        self.assertEqual(res.status_code, 200)

        res = self.client().patch(
            '/actors/1',
            headers=self.headers,
            json=self.otherActor)
        self.assertEqual(res.status_code, 200)

        res = self.client().patch(
            '/movies/5',
            headers=self.headers,
            json=self.otherMovie)
        self.assertEqual(res.status_code, 404)

        res = self.client().patch(
            '/actors/5',
            headers=self.headers,
            json=self.otherActor)
        self.assertEqual(res.status_code, 404)

    def testDELETE(self):
        res = self.client().delete('/movies/1')
        self.assertEqual(res.status_code, 401)

        res = self.client().delete('/actors/1')
        self.assertEqual(res.status_code, 401)

        res = self.client().delete(
            '/movies/5',
            headers=self.headers)
        self.assertEqual(res.status_code, 404)

        res = self.client().delete(
            '/actors/5',
            headers=self.headers)
        self.assertEqual(res.status_code, 404)

        res = self.client().delete(
            '/movies/1',
            headers=self.headers)
        self.assertEqual(res.status_code, 200)

        res = self.client().delete(
            '/actors/1',
            headers=self.headers)
        self.assertEquals(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
