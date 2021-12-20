from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from user_interface.serializers import UserSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def sign_up(request):
    """
    A sign-up view. Anyone can create an account providing
    their username and password.

    TODO:  human verification - robots shouldn't be allowed to create user accounts in a loop
    """
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return HttpResponse('OK')
