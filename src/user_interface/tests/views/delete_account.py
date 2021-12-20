from django.test import TestCase
from django.conf import settings
from rest_framework.test import APIClient
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from django.contrib.auth.models import User

api_base_url = settings.API_BASE_URL.strip('/')


class DeleteAccountTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create(
            username='user-1',
            email='user-1@example.com',
            password='pswd',
            first_name='user',
            last_name='one'
        )
        self.user.save()

    def test_patch(self):
        self.client.force_authenticate(self.user)

        response = self.client.delete(
            f'/{api_base_url}/delete-account'
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIsNone(
            User.objects.filter(username=self.user.username).first()
        )

    def test_unauthorized(self):
        response = self.client.delete(
            f'/{api_base_url}/delete-account'
        )
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
