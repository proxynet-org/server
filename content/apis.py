from rest_framework import viewsets
from .models import Message
from .serializers import MessageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from .utils import get_distance_from_two_locations


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        data['user'] = request.user
        user = User.objects.get(id=request.user.id)
        data['location'] = user.location
        data['idUser']=user.idUser
        self.perform_create(serializer)

        # return 201 status code
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        user = User.objects.get(id=request.user.id)
        new_queryset = []
        for message in queryset:
            distance = get_distance_from_two_locations(
                message.location, user.location)
            if distance <= 5:
                new_queryset.append(message)

        serializer = self.get_serializer(new_queryset, many=True)
        return Response(serializer.data)
