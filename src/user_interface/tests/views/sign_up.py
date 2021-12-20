from django.test import TestCase
from django.conf import settings
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.test import APIClient

from user_interface.models import User

api_base_url = settings.API_BASE_URL.strip('/')


class SignUpViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_post(self):
        test_username = 'test-user'
        test_password = 'test-pswd'

        response = self.client.post(
            f'/{api_base_url}/sign_up',
            {
                'username': test_username,
                'password': test_password
            }
        )
        self.assertEqual(response.status_code, HTTP_200_OK)

        new_user = User.objects.get(username=test_username)
        self.assertIsInstance(new_user, User)

    def test_missing_password(self):
        response = self.client.post(
            f'/{api_base_url}/sign_up',
            {
                'username': 'test-user'
            }
        )
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_unique_user(self):
        test_username = 'test-user'
        test_password = 'test-pswd'

        response = self.client.post(
            f'/{api_base_url}/sign_up',
            {
                'username': test_username,
                'password': test_password
            }
        )
        self.assertEqual(response.status_code, HTTP_200_OK)

        response = self.client.post(
            f'/{api_base_url}/sign_up',
            {
                'username': test_username,
                'password': test_password
            }
        )
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
