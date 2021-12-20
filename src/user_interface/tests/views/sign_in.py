import mock

from django.conf import settings
from rest_framework.status import HTTP_200_OK

from .oauth2_proxy_test_case import OAuth2ProxyTestCase

api_base_url = settings.API_BASE_URL.strip('/')


class SignInViewTest(OAuth2ProxyTestCase):
    def test_post(self):
        with mock.patch('requests.post') as mock_request:
            mock_request.return_value = self.mock_oauth2_response
            response = self.client.post(
                f'/{api_base_url}/sign_in',
                {
                    'username': self.user.username,
                    'password': self.user.password
                }
            )
            mock_request.assert_called_with(
                f'{settings.OAUTH2_URL}/token/',
                data={
                    'grant_type': 'password',
                    'username': self.user.username,
                    'password': self.user.password,
                    'client_id': self.app.client_id,
                    'client_secret': self.app.client_secret
                })
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(
            response.json(),
            self.mock_oauth2_response.json()
        )
