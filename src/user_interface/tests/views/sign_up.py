import mock

from django.test import TestCase
from django.conf import settings
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.test import APIClient
from oauth2_provider.models import Application
from django.contrib.auth.models import User

api_base_url = settings.API_BASE_URL.strip('/')


class SignUpViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.mock_oauth2_response = mock.MagicMock()
        self.mock_oauth2_response.json.return_value = {
            'access_token': '<an-ephemeral-token>',
            'expires_in': 36000,
            'token_type': 'Bearer',
            'scope': 'read write groups',
            'refresh_token': '<a-lasting-token>'
        }

        self.admin = User.objects.create(
            username='admin',
            email='admin@example.com',
            password='pswd'
        )
        self.admin.save()

        self.app = Application.objects.create(
            name='user_interface',
            user=self.admin,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
        )
        self.app.save()

    def test_post(self):
        test_username = 'test-user'
        test_password = 'test-pswd'

        with mock.patch('requests.post') as mock_request:
            mock_request.return_value = self.mock_oauth2_response
            response = self.client.post(
                f'/{api_base_url}/sign_up',
                {
                    'username': test_username,
                    'password': test_password
                }
            )
            mock_request.assert_called()
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

        with mock.patch('requests.post') as mock_request:
            mock_request.return_value = self.mock_oauth2_response
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
