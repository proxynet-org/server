from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.renderers import JSONRenderer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@renderer_classes([JSONRenderer])
def update_user_location(request, *args, **kwargs):
    user = User.objects.get(id=request.user.id)
    coordinates = request.data['coordinates']
    user.coordinates = coordinates
    user.save()
    return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@renderer_classes([JSONRenderer])
def get_user_info(request, *args, **kwargs):
    user = User.objects.get(id=request.user.id)
    return Response(status=status.HTTP_200_OK, data={
        'username': user.username,
        'coordinates': user.coordinates,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'id': user.id,
    })