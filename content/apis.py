from rest_framework import viewsets
from .models import Message, PrivateMessage, Publication, Comment
from .serializers import MessageSerializer, PrivateMessageSerializer, PublicationSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from .utils import get_distance_from_two_coordinates
from django.conf import settings
import websocket
from django.urls import reverse
from django.db.models import Q


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

        try:
            socket = reverse('websocket', kwargs={'room_name': "publications"})
            socket_url = settings.WEBSOCKET_URL + socket
            ws = websocket.WebSocket()
            ws.connect(socket_url)
            ws.close()
        except:
            print("Error connecting to websocket, or wrong url specified in settings.py")

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def list(self, request, *args, **kwargs):
        # only show publications from users within 100km
        user = User.objects.get(id=request.user.id)
        publications = Publication.objects.all()
        publications_within_range = []
        range = settings.RADIUS_FOR_SEARCH
        for publication in publications:
            distance = get_distance_from_two_coordinates(
                user.coordinates, publication.coordinates)
            if distance <= range:
                publications_within_range.append(publication)
        # add reaction field to each publication
        for publication in publications_within_range:
            if user in publication.likes.all():
                publication.reaction = 'LIKE'
            elif user in publication.dislikes.all():
                publication.reaction = 'DISLIKE'
            else:
                publication.reaction = 'NONE'
        serializer = self.get_serializer(publications_within_range, many=True)
        return Response(serializer.data)

    def like(self, request, *args, **kwargs):
        # get the publication id from the url <int:pk>
        publication_id = kwargs['pk']
        # get the publication
        publication = Publication.objects.get(id=publication_id)
        # get the user
        user = User.objects.get(id=request.user.id)
        # add the user to the likes
        if user in publication.likes.all():
            publication.likes.remove(user)
        else :
            publication.likes.add(user)
        if user in publication.dislikes.all():
            publication.dislikes.remove(user)
        # return the publication
        serializer = PublicationSerializer(publication)
        return Response(serializer.data)
    
    def dislike(self, request, *args, **kwargs):
        # get the publication id from the url <int:pk>
        publication_id = kwargs['pk']
        # get the publication
        publication = Publication.objects.get(id=publication_id)
        # get the user
        user = User.objects.get(id=request.user.id)
        # add the user to the dislikes
        if user in publication.dislikes.all():
            publication.dislikes.remove(user)
        else :
            publication.dislikes.add(user)
        if user in publication.likes.all():
            publication.likes.remove(user)
        # return the publication
        serializer = PublicationSerializer(publication)
        return Response(serializer.data)

    def list_comments(self, request, *args, **kwargs):
        # get the publication id from the url <int:pk>
        publication_id = kwargs['pk']
        # get the publication
        publication = Publication.objects.get(id=publication_id)
        # get the comments and is_reply=False
        comments = Comment.objects.filter(Q(publication=publication) & Q(is_reply=False)).order_by('created_at')
        # get user reaction
        user = User.objects.get(id=request.user.id)
        for comment in comments:
            if user in comment.likes.all():
                comment.reaction = 'LIKE'
            elif user in comment.dislikes.all():
                comment.reaction = 'DISLIKE'
            else:
                comment.reaction = 'NONE'
        # return the comments
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def list_comments_of_comments(self, request, *args, **kwargs):
        # get the comment id from the url <int:pk>
        comment_id = kwargs['pkComment']
        # get the comment
        comment = Comment.objects.get(id=comment_id)
        # get the comments
        comments = Comment.objects.filter(parent_comment=comment).order_by('created_at')
        # get user reaction
        user = User.objects.get(id=request.user.id)
        for comment in comments:
            if user in comment.likes.all():
                comment.reaction = 'LIKE'
            elif user in comment.dislikes.all():
                comment.reaction = 'DISLIKE'
            else:
                comment.reaction = 'NONE'
        # return the comments
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def add_comment(self, request, *args, **kwargs):
        # get the publication id from the url <int:pk>
        publication_id = kwargs['pk']
        # get the publication
        publication = Publication.objects.get(id=publication_id)
        # get the text
        text = request.data['text']
        # get the coordinates
        user = User.objects.get(id=request.user.id)
        # create the comment
        comment = Comment.objects.create(
            publication=publication, text=text, user=user)
        # return the comment
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def add_comment_reply(self, request, *args, **kwargs):
        # get the comment id from the url <int:pk>
        comment_id = kwargs['pkComment']
        # get the comment
        comment = Comment.objects.get(id=comment_id)
        # get the text
        text = request.data['text']
        # get the coordinates
        user = User.objects.get(id=request.user.id)
        # create the comment
        comment = Comment.objects.create(
            user=user, publication=comment.publication, text=text, parent_comment=comment, is_reply=True)
        # return the comment
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def like_comment(self, request, *args, **kwargs):
        # get the comment id from the url <int:pk>
        comment_id = kwargs['pkComment']
        # get the comment
        comment = Comment.objects.get(id=comment_id)
        # get the user
        user = User.objects.get(id=request.user.id)
        # add the user to the likes
        if user in comment.likes.all():
            comment.likes.remove(user)
        else :
            comment.likes.add(user)
        if user in comment.dislikes.all():
            comment.dislikes.remove(user)
        # return the comment
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def dislike_comment(self, request, *args, **kwargs):
        # get the comment id from the url <int:pk>
        comment_id = kwargs['pkComment']
        # get the comment
        comment = Comment.objects.get(id=comment_id)
        # get the user
        user = User.objects.get(id=request.user.id)
        # add the user to the dislikes
        if user in comment.dislikes.all():
            comment.dislikes.remove(user)
        else :
            comment.dislikes.add(user)
        if user in comment.likes.all():
            comment.likes.remove(user)
        # return the comment
        serializer = CommentSerializer(comment)
        return Response(serializer.data)