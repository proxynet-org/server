from rest_framework import viewsets
from .models import Zone, Chatroom, ChatroomMessages
from .serializers import ZoneSerializer, ChatroomSerializer
from content.serializers import MessageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from django.conf import settings
from content.utils import get_distance_from_two_coordinates

class ZoneViewSet(viewsets.ModelViewSet):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer


class ChatroomViewSet(viewsets.ModelViewSet):
    queryset = Chatroom.objects.all()
    serializer_class = ChatroomSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(id=request.user.id)
        data = serializer.validated_data
        data["capacity"] = int(request.data["capacity"])
        data["lifetime"] = int(request.data["lifetime"])
        data['coordinates'] = user.coordinates
        self.perform_create(serializer)

        # return 201 status code
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request):
        user = User.objects.get(id=request.user.id)
        range = settings.RADIUS_FOR_SEARCH
        chatrooms = Chatroom.objects.all()
        chatrooms_in_range = []
        for chatroom in chatrooms:
            distance = get_distance_from_two_coordinates(user.coordinates, chatroom.coordinates)
            if distance <= range:
                chatrooms_in_range.append(chatroom)
        serializer = ChatroomSerializer(chatrooms_in_range, many=True, context={'request': request})  
        return Response(serializer.data)

    def join_chatroom(self, request, pk=None):
        user = User.objects.get(id=request.user.id)
        user_coordinates = user.coordinates
        distance = get_distance_from_two_coordinates(user_coordinates, Chatroom.objects.get(id=pk).coordinates)
        chatroom = Chatroom.objects.get(id=pk)
        if chatroom.is_open and chatroom.is_available and user.is_in_chatroom == False and distance <= settings.RADIUS_FOR_SEARCH and chatroom.current_users.count() < chatroom.capacity:
            chatroom.current_users.add(user)
            chatroom.save()
            user.is_in_chatroom = True
            user.save()
            if chatroom.current_users.count() == chatroom.capacity:
                chatroom.is_available = False
                chatroom.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def leave_chatroom(self, request, pk=None):
        user = User.objects.get(id=request.user.id)
        chatroom = Chatroom.objects.get(id=pk)
        if user in chatroom.current_users.all():
            chatroom.current_users.remove(user)
            chatroom.save()
            user.is_in_chatroom = False
            user.save()
            if chatroom.current_users.count() < chatroom.capacity:
                chatroom.is_available = True
                chatroom.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def send_message_to_chatroom(self, request, pk=None):
        user = User.objects.get(id=request.user.id)
        chatroom = Chatroom.objects.get(id=pk)
        coordinates = chatroom.coordinates
        message = request.data['text']
        if user in chatroom.current_users.all():
            msg = ChatroomMessages.objects.create(user=user, chatroom=chatroom, text=message, coordinates=coordinates)
            msg.save()
            chatroom.messages.add(msg)
            serializer = MessageSerializer(msg)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def list_messages(self, request, pk=None):
        chatroom = Chatroom.objects.get(id=pk)
        user = User.objects.get(id=request.user.id)
        if user in chatroom.current_users.all():
            messages = chatroom.messages.all()
            return Response(MessageSerializer(messages, many=True).data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

