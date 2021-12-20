from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_details(request):
    """
    Updates details for the currently logged-in user.
    Any of the following can be updated by providing
    corresponding keys within the request:
        username
        password
        first_name
        last_name
    """

    current_user = request.user

    new_password = request.data.get('password')
    if new_password:
        current_user.set_password(new_password)

    for key in ('username', 'first_name', 'last_name'):
        new_value = request.data.get(key)
        if new_value:
            setattr(current_user, key, new_value)

    current_user.save()
    return HttpResponse('OK')
