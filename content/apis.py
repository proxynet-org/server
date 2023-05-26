from rest_framework import viewsets
from .models import Message, PrivateMessage, Publication
from .serializers import MessageSerializer, PrivateMessageSerializer, PublicationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from .utils import get_distance_from_two_coordinates
from django.conf import settings
import websocket
from django.urls import reverse

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        data['user'] = request.user
        user = User.objects.get(id=request.user.id)
        data['coordinates'] = user.coordinates
        self.perform_create(serializer)

        # return 201 status code
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        # only show messages from users within 100km
        user = User.objects.get(id=request.user.id)
        messages = Message.objects.all()
        messages_within_range = []
        range = settings.RADIUS_FOR_SEARCH
        for message in messages:
            distance = get_distance_from_two_coordinates(
                user.coordinates, message.coordinates)
            if distance <= range:
                messages_within_range.append(message)
        serializer = self.get_serializer(messages_within_range, many=True)
        return Response(serializer.data)


class PrivateMessageViewSet(viewsets.ModelViewSet):
    queryset = PrivateMessage.objects.all()
    serializer_class = PrivateMessageSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        # get the sender
        sender = User.objects.get(id=request.user.id)
        # get the receiver
        receiver = User.objects.get(id=request.data['receiver'])
        # get the text
        text = request.data['text']
        # get the coordinates
        coordinates = sender.coordinates

        # create the message
        message = PrivateMessage.objects.create(
            sender=sender, receiver=receiver, text=text, coordinates=coordinates)

        # return 201 status code
        serializer = self.get_serializer(message)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def view_convo_with_receiver(self, request, *args, **kwargs):
        # get the receiver id from the url <int:pk>
        receiver_id = kwargs['pk']
        # get the receiver
        receiver = User.objects.get(id=receiver_id)
        # get the sender
        sender = User.objects.get(id=request.user.id)
        # get the messages
        messages = PrivateMessage.objects.filter(
            sender=sender, receiver=receiver).order_by('created_at')
        # return the messages
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)

class PublicationViewSet(viewsets.ModelViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        data['user'] = request.user
        user = User.objects.get(id=request.user.id)
        data['coordinates'] = user.coordinates
        self.perform_create(serializer)

        # return 201 status code
        headers = self.get_success_headers(serializer.data)

        socket = reverse('websocket', kwargs={'room_name': "publications"})
        socket_url = f"ws://localhost:8000{socket}"

        signal = {
            "message" : "Post has been created",
            "coordinates" : data["coordinates"]
        }

        ws = websocket.WebSocket()
        ws.connect(socket_url)
        ws.send(str(signal))
        ws.close()


        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
