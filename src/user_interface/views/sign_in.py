import requests

from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from oauth2_provider.models import Application


@api_view(['POST'])
@permission_classes([AllowAny])
def sign_in(request):
    """
    A sign-in view. Anyone can create an account
    providing their username and password.

    TODO:  request throttling - prevent brute force

    :returns:   json response with the auth tokens, format:
        {
            'access_token': '<temporary-token: str>',
            'expires_in': '<duration: int>',
            'token_type': 'Bearer',
            'scope': <str>,
            'refresh_token': '<lasting-token: str>'
        }
    """
    current_app = Application.objects.get(name='user_interface')

    oauth2_response = requests.post(
        f'{settings.OAUTH2_URL}/token/',
        data={
            'grant_type': 'password',
            'username': request.data.get('username'),
            'password': request.data.get('password'),
            'client_id': current_app.client_id,
            'client_secret': current_app.client_secret
        }
    )

    return JsonResponse(oauth2_response.json())
