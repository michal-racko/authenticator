import requests

from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from oauth2_provider.models import Application

from user_interface.serializers import UserSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def sign_up(request) -> JsonResponse:
    """
    A sign-up view. Anyone can create an account
    providing their username and password.

    TODO:  human verification - robots shouldn't be allowed to create user accounts in a loop

    :returns:   json response with the auth tokens, format:
        {
            'access_token': '<temporary-token: str>',
            'expires_in': '<duration: int>',
            'token_type': 'Bearer',
            'scope': <str>,
            'refresh_token': '<lasting-token: str>'
        }
    """
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    current_app = Application.objects.get(name='user_interface')

    oauth2_response = requests.post(
        f'{settings.OAUTH2_URL}/token/',
        data={
            'grant_type': 'password',
            'username': request.data['username'],
            'password': request.data['password'],
            'client_id': current_app.client_id,
            'client_secret': current_app.client_secret
        }
    )

    return JsonResponse(
        oauth2_response.json(),
        status=oauth2_response.status_code
    )
