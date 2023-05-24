from rest_framework import viewsets
from .models import Message, PrivateMessage, Publication
from .serializers import MessageSerializer, PrivateMessageSerializer, PublicationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users.models import User

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
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
