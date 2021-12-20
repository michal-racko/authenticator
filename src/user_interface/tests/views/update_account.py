from django.test import TestCase
from django.conf import settings
from rest_framework.test import APIClient
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from django.contrib.auth.models import User

api_base_url = settings.API_BASE_URL.strip('/')


class UpdateAccountTest(TestCase):
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

        new_name = 'new-name'
        response = self.client.patch(
            f'/{api_base_url}/update-account',
            data={
                'first_name': new_name
            }
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
        User.objects.get(first_name=new_name)

    def test_unauthorized(self):
        new_name = 'new-name'
        response = self.client.patch(
            f'/{api_base_url}/update-account',
            data={
                'first_name': new_name
            }
        )
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
