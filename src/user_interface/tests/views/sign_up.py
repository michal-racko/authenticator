import mock

from django.conf import settings
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.contrib.auth.models import User

from .oauth2_proxy_test_case import OAuth2ProxyTestCase

api_base_url = settings.API_BASE_URL.strip('/')


class SignUpViewTest(OAuth2ProxyTestCase):
    def test_post(self):
        test_username = 'test-user'
        test_password = 'test-pswd'

        with mock.patch('requests.post') as mock_request:
            mock_request.return_value = self.mock_oauth2_response
            response = self.client.post(
                f'/{api_base_url}/sign-up',
                {
                    'username': test_username,
                    'password': test_password
                }
            )
            mock_request.assert_called_with(
                f'{settings.OAUTH2_URL}/token/',
                data={
                    'grant_type': 'password',
                    'username': test_username,
                    'password': test_password,
                    'client_id': self.app.client_id,
                    'client_secret': self.app.client_secret
                })
        self.assertEqual(response.status_code, HTTP_200_OK)

        new_user = User.objects.get(username=test_username)
        self.assertIsInstance(new_user, User)

    def test_missing_password(self):
        response = self.client.post(
            f'/{api_base_url}/sign-up',
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
                f'/{api_base_url}/sign-up',
                {
                    'username': test_username,
                    'password': test_password
                }
            )
        self.assertEqual(response.status_code, HTTP_200_OK)

        response = self.client.post(
            f'/{api_base_url}/sign-up',
            {
                'username': test_username,
                'password': test_password
            }
        )
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
