import unittest
import warnings

from flask import url_for
from flask_testing import TestCase
from flask_jwt_extended import create_access_token

from web import app, db
from web.models import User


class TestAuth(TestCase):

    def create_app(self):
        warnings.simplefilter('ignore', category=DeprecationWarning)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['SECRET_KEY'] = 'secret'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        db.create_all()
        self. data = {'email': 'test1@example.com', 'password': 'password', 'username': 'username1'}

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_signup(self):
        """Test signing up for new user"""
        # Init user data
        data = self.data.copy()
        data['confirm_password'] = data['password']
        # Send a POST request to the REST API to create new account
        response = self.client.post(url_for('signup'), data=data)
        # Check that the response has a 201 CREATED status code
        self.assertEqual(response.status_code, 201)
        # Check that the user is successfully created
        self.assertIn(b'User has successfully created', response.data)
        user = User.query.filter_by(email=data['email']).first()
        # Check that the user is located in database
        self.assertIsNotNone(user)

    def test_login(self):
        """Test logging in an existing user"""
        # Create new user & commit to the database
        data = self.data
        user = User.create_user(**data)
        db.session.add(user)
        db.session.commit()
        # Send a POST request to the REST API to login & get access token
        response = self.client.post(url_for('login'),
                                    data={k: v for k, v in data.items() if k in ('email', 'password')})
        # Check that the response has a 200 OK status code
        self.assert200(response)
        # Check that the access token is returned
        self.assertIn(b'access_token', response.data)

    def test_invalid_login(self):
        """Test logging in with invalid credentials"""
        # Create new user & commit to the database
        user = User.create_user(email='test3@example.com', password='password', username='username3')
        db.session.add(user)
        db.session.commit()
        data = user.as_dict()
        # Update password to a different value
        data['password'] = 'wrong_password'
        # Send a POST request to the REST API to login
        response = self.client.post(url_for('login'), data={k: v for k, v in data.items() if k in ('email', 'password')})
        # Check that the response has a 401 UNAUTHORIZED status code
        self.assert401(response)
        # Check that invalid message is returned
        self.assertIn(b'Invalid email or password', response.data)

    def test_delete(self):
        # Create new user & commit to the database
        user = User.create_user(email='test3@example.com', password='password', username='username3')
        db.session.add(user)
        db.session.commit()
        # Create Access Token
        token = create_access_token(identity=user.id)
        # Send a DELETE request to the REST API to remove the user
        delete_url = url_for('delete', user_id=user.id)
        response = self.client.delete(delete_url, headers={'Authorization': 'Bearer ' + token})
        # Assert the response status code is 200 (successful)
        self.assert200(response)
        # Assert the response message is as expected
        expected_response = {'message': 'User has successfully delete'}
        self.assertEqual(response.json, expected_response)
        # Assert the user is deleted from the database
        deleted_user = db.session.get(User, user.id)
        self.assertIsNone(deleted_user)


class TestJobMatching(TestCase):

    def create_app(self):
        warnings.simplefilter('ignore', category=DeprecationWarning)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['SECRET_KEY'] = 'secret'
        app.config['TESTING'] = True
        return app

    def setUp(self):
        db.create_all()
        # Create a test user
        data = {'email': 'test@example.com', 'password': 'password', 'username': 'username'}
        user = User.create_user(**data)
        # Commit to the database
        db.session.add(user)
        db.session.commit()
        # Create a token for the newly added user
        self.access_token = create_access_token(identity=user.id)
        # Init the required test data
        self.data = {
            "location": "United States",
            "keywords": ["Python", "SQL"],
            "education": "Bachelor's Degree",
            "skills":  ["Python", "SQL", "Data Analysis"],
            "start": 25
        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def get_auth_headers(self):
        return {'Authorization': 'Bearer ' + self.access_token}

    def test_test_missed_data(self):
        # Send a GET request to the job_matching endpoint without test data
        response = self.client.get(url_for('job_matching'), headers=self.get_auth_headers())
        # Assert that response has a 400 status code
        self.assert400(response)

    def test_unauthorized_access(self):
        # Send a GET request to the job_matching endpoint with test data, ignoring the headers for authentications
        response = self.client.get(url_for('job_matching'), data=self.data)
        # Assert that response has a 401 status code
        self.assert401(response)

    def test_job_matching(self):
        # Send a GET request to the job_matching endpoint with test data and headers for authentications
        response = self.client.get(url_for('job_matching'), data=self.data, headers=self.get_auth_headers())
        # Assert that response has a 200 status code
        self.assert200(response)
        # Assert that the response data is a list of dictionaries
        self.assertIsInstance(response.json['job_listings'], list)


if __name__ == '__main__':
    unittest.main()
