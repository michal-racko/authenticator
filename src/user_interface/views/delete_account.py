from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    """
    Deletes the given user's account.
    """
    current_user = request.user
    current_user.delete()
    return HttpResponse('OK')
