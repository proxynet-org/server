from rest_framework import serializers
from .models import Message, PrivateMessage, Publication


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id','user', 'text', 'created_at', 'updated_at', 'coordinates')
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'coordinates': {'read_only': True},
        }

class PrivateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateMessage
        fields = ('id','sender', 'receiver', 'text', 'created_at', 'updated_at', 'coordinates')
        extra_kwargs = {
            'id': {'read_only': True},
            'sender': {'read_only': True},
            #'receiver': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'coordinates': {'read_only': True},
        }

class PublicationSerializer(serializers.ModelSerializer):
    # num_likes counts the items in likes
    num_likes = serializers.SerializerMethodField()
    class Meta:
        model = Publication
        fields = ('id','user', 'title', 'text', 'likes', 'dislikes', 'comments', 'created_at', 'updated_at', 'coordinates', 'image' , 'num_likes')
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
            'likes': {'read_only': True},
            'dislikes': {'read_only': True},
            'comments': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'coordinates': {'read_only': True},
        }
    def get_num_likes(self, obj):
        return len(obj.likes.all())
