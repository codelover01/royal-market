import unittest
#from app import app
app = __import__('app').app
from models import db
from models.users import User


class TestApp(unittest.TestCase):
    """ Represents the TestApp class """
    def setUp(self):
        """ Set up test client and test database. """
        app.config['TESTING'] = True # Enable testing mode
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory database for testing
        self.client = app.test_client()

        with app.app_context():
            db.create_all()


    def tearDown(self):
        """ clean up after each test. """
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_user(self):
        """Test creating a new user via the API endpoint."""
        response = self.client.post(
            '/auth/register',
            json={
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'securepassword123'
                })
        self.assertEqual(response.status_code, 201) # 201 created
        data = response.get_json()
        self.assertEqual(data['username'], 'testuser')
        self.assertEqual(data['email'], 'test@example.com')


if __name__ == '__main__':
    unittest.main()