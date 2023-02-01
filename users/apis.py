from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.renderers import JSONRenderer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@renderer_classes([JSONRenderer])
def update_user_location(request, *args, **kwargs):
    """
    expected json data
    {
        "location": "48.856614,2.3522219"
    }
    """
    user = User.objects.get(id=request.user.id)
    # retrive location from post data
    user.location = request.POST.get('location')
    user.save()
    return Response(status=status.HTTP_200_OK)
