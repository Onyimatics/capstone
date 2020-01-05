
import os
import unittest
import json

from app import create_app
from models import setup_db, Movie, Actor

EXECUTIVE_PRODUCER = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJqQkdRVGMwTkRBd016WkNOek5DUVRjeU5VUXdOVGRHTVVKR01UQXhNekU0TkVORU4wVkJOUSJ9.eyJpc3MiOiJodHRwczovL2p1bGl1cy1jemFyLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZTAxZWFhNDE0ZWIyYTBkZDI5NWZiYjYiLCJhdWQiOiJtb3ZpZSIsImlhdCI6MTU3NzE4NzUwNCwiZXhwIjoxNTc3MTk0NzA0LCJhenAiOiI0S3FjeHFWbklXd0ZFRkRlNjBwdHNEVUVBZDVaUDZORyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.XQm7Un98iCO9EXgUxr5Ond_5U1No1CtTEqP9mLrOchgYe2Dx-59ujxTM6c0ETk0VJey8HwbE0pSnpfNuMco0TrFb3FEbfg6bb47KSEmJQqeNn5TKA0u-DSqdEOcLvoCrJ1NFZgRdzYe9wfZjtYw7N804ClnbmK0ulIzYDjG2-3SUByiekoc31ZVPwSfIa178lTKXDGczdzkIO3Hr0MStGVcabS-WtUY3iPQ2g-A_XZjtYGlFxmWV_zucR6QX1RCW6mTleNAxPeDkpH_u8p80c6hU7tk8vW_GBVHceoA-e7r9JnGBEf4rp31wpRqKNKjwzG5dP6I5v6UrJRrb93iS0Q'

CASTING_DIRECTOR = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJqQkdRVGMwTkRBd016WkNOek5DUVRjeU5VUXdOVGRHTVVKR01UQXhNekU0TkVORU4wVkJOUSJ9.eyJpc3MiOiJodHRwczovL2p1bGl1cy1jemFyLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZGZjOWYyNjk0ZDdhNTE1MzY1ZjdhMzgiLCJhdWQiOiJtb3ZpZSIsImlhdCI6MTU3NzE4NDEwNiwiZXhwIjoxNTc3MTkxMzA2LCJhenAiOiI0S3FjeHFWbklXd0ZFRkRlNjBwdHNEVUVBZDVaUDZORyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.o_0mfhGHdoIUHME_mfJES95nZucLCVtOIoo8Cf7pnpJPe0BgK2fzLZQbyFzXC5E780t3kguQHhd_sdwd2Xp5t51cURGVDN8oRG43qjsOtg0k7AsAXp0y9X6JxfueUE7NNlKs7WPVwYcHWBjOaNlaaV54zYwjmOh0NU8YBfTTA2zRHcyr8JIBJsw-8pPxRSjErnyXJoprDJMVYT-AppSnLHADd9zbKjQ3Ags0bVgzWqSJlsqJojErYA2ZraCc3hNeElx7VSmqSHnr_JUYWn1V2rNEtXCHhdHVLOvp3xDAn5AGCgXADWw_ESvXZqbJRL2I32nN3KSBO9cr24h1M9XIFA'

CASTING_ASSISTANT = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJqQkdRVGMwTkRBd016WkNOek5DUVRjeU5VUXdOVGRHTVVKR01UQXhNekU0TkVORU4wVkJOUSJ9.eyJpc3MiOiJodHRwczovL2p1bGl1cy1jemFyLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZGZjOWZmNDk0ZDdhNTE1MzY1ZjdhNDEiLCJhdWQiOiJtb3ZpZSIsImlhdCI6MTU3NzE4NDIwMiwiZXhwIjoxNTc3MTkxNDAyLCJhenAiOiI0S3FjeHFWbklXd0ZFRkRlNjBwdHNEVUVBZDVaUDZORyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.Mtop1a84CuIHV9fEuCIHJ47I2JMdL0iQzW32992s8HFUiE-jE-yfNeucA0esCdAFWrjzakro1KwRr60s2VMz9PwPmBcP1d1bZ1PeViP8r3WKMBiE3sCMf3lqLNia9wz7vbioRDR8pGOrYh_CcUH-WSudCfDK0ZhdqlsKFITPVgtOdB26_eFdARfKQvmyrqAkEM6EpX6ssf7jR7x3h-koVuJgM8JLLjame0kb3GuZ10znlLKyircj9hq71vLFo8oOoD_ExJnscchf5NK_qmtnZ67UmFp9e0WXlk-Y4rWwt-rrgkytsdF4VISycDAtgQdeTRO8-ZbNwtPIE_5OKPR1Ig'


class MHTestCase(unittest.TestCase):
    """This class represents the movies-hub test case"""
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['TEST_DB_URL']

        setup_db(self.app, self.database_path)

    def tearDown(self):
        """Executed after reach test"""
        pass

#####################    MOVIE TEST STARTS #################################################

    #  GET /movies
    def test_get_movies(self):
        response = self.client().get(
            '/movies',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    # GET /movies/id
    def test_get_movie_byId(self):
        response = self.client().get(
            '/movies/1',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['title'], 'Nikita')

    def test_get_movie_byId_404(self):
        response = self.client().get(
            '/movies/333333',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertEqual(data['message'], 'Resource not found')

    # POST /movies
    def test_post_movie(self):
        response = self.client().post(
            '/movies',
            json={'title': 'Sigidi', 'release_date': "2017-02-19"},
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Movie created successfully')
        self.assertEqual(data['movie']['title'], 'Sigidi')

    def test_post_movie_400(self):
        response = self.client().post(
            '/movies',
            json={'title': '', 'release_date': ""},
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request, pls check your inputs')

    def test_post_movie_401(self):
        response = self.client().post(
            '/movies',
            json={'title': 'Unauthorize movie', 'release_date': "2019-12-23"},
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message']['code'], 'unauthorized')

    # PATCH /movies
    def test_edit_movie(self):
        response = self.client().patch(
            '/movies/2',
            json={'title': 'The Squash', 'release_date': "2000-10-19"},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Movie updated')
        self.assertEqual(data['movie']['title'], 'The Squash')


    def test_edit_movie_400(self):
        response = self.client().patch(
            '/movies/1',
            json={'title': '', 'release_date': ""},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request, pls check your inputs')


    def test_edit_movie_404(self):
        response = self.client().patch(
            '/movies/4444444',
            json={'title': 'New Life', 'release_date': "2003-09-16"},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')


    # DELETE /movies/id
    def test_delete_movie(self):
        response = self.client().delete(
            '/movies/3',
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Movie deleted successfully')

    def test_delete_movie_404(self):
        response = self.client().delete(
            '/movies/11111111',
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_delete_movie_401(self):
        response = self.client().delete(
            '/movies/1',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message']['code'], 'unauthorized')

#####################    MOVIE TEST ENDS #################################################



#####################    ACTORS TEST START #################################################
    #  GET /actors
    def test_get_actors(self):
        response = self.client().get(
            '/actors',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])


    # GET /actors/id
    def test_get_actor_byId(self):
        response = self.client().get(
            '/actors/1',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertEqual(data['actor']['name'], 'Arnold Swaztnigger')

    def test_get_actor_byId_404(self):
        response = self.client().get(
            '/actors/121234',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertEqual(data['message'], 'Resource not found')

    # POST /actors
    def test_post_actor(self):
        response = self.client().post(
            '/actors',
            json={'name': 'Julius', 'age': 24, "gender": "male"},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Actor added')
        self.assertEqual(data['actor']['name'], 'Julius')


    def test_post_actor_400(self):
        response = self.client().post(
            '/actors',
            json={'name': '', 'age': '', "gender": ""},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request, pls check your inputs')

    
    def test_post_actor_401(self):
        response = self.client().post(
            '/actors',
            json={'name': 'Czar', 'age': 14, "gender": "female"},
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message']['code'], 'unauthorized')

    # PATCH /actors
    def test_edit_actor(self):
        response = self.client().patch(
            '/actors/2',
            json={'name': 'Emily', 'age': 37, "gender": "male"},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Actor updated')
        self.assertEqual(data['actor']['name'], 'Emily')

    def test_edit_actor_400(self):
        response = self.client().patch(
            '/actors/2',
            json={'name': '', 'age': '', "gender": ""},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request, pls check your inputs')


    def test_edit_actor_404(self):
        response = self.client().patch(
            '/actors/9999999',
            json={'name': 'Mike', 'age': 65, "gender": "male"},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')


    # DELETE /actors/id
    def test_delete_actor(self):
        response = self.client().delete(
            '/actors/3',
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Actor deleted successfully')

    
    def test_delete_actor_401(self):
        response = self.client().delete(
            '/actors/2',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message']['code'], 'unauthorized')

    
    def test_delete_actor_404(self):
        response = self.client().delete(
            '/actors/545432',
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()