import mock

from django.test import TestCase
from django.conf import settings
from rest_framework.test import APIClient
from oauth2_provider.models import Application
from django.contrib.auth.models import User

api_base_url = settings.API_BASE_URL.strip('/')


class OAuth2ProxyTestCase(TestCase):
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
        self.mock_oauth2_response.status_code = 200

        self.user = User.objects.create(
            username='user-1',
            email='user-1@example.com',
            password='pswd'
        )
        self.user.save()

        self.app = Application.objects.get(
            name='user_interface'
        )
