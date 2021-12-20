import requests

from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from oauth2_provider.models import Application


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh(request):
    """
    Provides a new access token if the given refresh_token is valid.

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
            'grant_type': 'refresh_token',
            'refresh_token': request.data.get('refresh_token'),
            'client_id': current_app.client_id,
            'client_secret': current_app.client_secret
        }
    )

    return JsonResponse(
        oauth2_response.json(),
        status=oauth2_response.status_code
    )
