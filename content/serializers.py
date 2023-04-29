from rest_framework import serializers
from .models import Message, PrivateMessage, Publication


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('user', 'text', 'created_at', 'updated_at', 'location')
        extra_kwargs = {
            'user': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'location': {'read_only': True},
        }

class PrivateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateMessage
        fields = ('sender', 'receiver', 'text', 'created_at', 'updated_at', 'location')
        extra_kwargs = {
            'sender': {'read_only': True},
            #'receiver': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'location': {'read_only': True},
        }

class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = ('user', 'text', 'created_at', 'updated_at', 'location')
        extra_kwargs = {
            'user': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'location': {'read_only': True},
        }