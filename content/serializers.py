from rest_framework import serializers
from .models import Message, PrivateMessage, Publication, Comment


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'user', 'text', 'created_at',
                  'updated_at', 'coordinates')
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
        fields = ('id', 'sender', 'receiver', 'text',
                  'created_at', 'updated_at', 'coordinates')
        extra_kwargs = {
            'id': {'read_only': True},
            'sender': {'read_only': True},
            # 'receiver': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'coordinates': {'read_only': True},
        }


class PublicationSerializer(serializers.ModelSerializer):
    # num_likes counts the items in likes
    num_likes = serializers.SerializerMethodField()
    num_dislikes = serializers.SerializerMethodField()
    num_comments = serializers.SerializerMethodField()
    reaction = serializers.SerializerMethodField()

    class Meta:
        model = Publication
        fields = ('id', 'user', 'title', 'text', 'likes', 'dislikes', 'created_at',
                  'updated_at', 'coordinates', 'image', 'num_likes', 'reaction', 'num_dislikes', 'num_comments')
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
            'likes': {'read_only': True},
            'dislikes': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'coordinates': {'read_only': True},
        }

    def get_num_likes(self, obj):
        return len(obj.likes.all())

    def get_num_dislikes(self, obj):
        return len(obj.dislikes.all())
    
    def get_num_comments(self, obj):
        return len(Comment.objects.filter(publication=obj))
    
    def get_reaction(self, obj):
        user = self.context['request'].user
        if user in obj.likes.all():
            return 'LIKE'
        elif user in obj.dislikes.all():
            return 'DISLIKE'
        else:
            return 'NONE'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'user', 'publication', 'text', 'created_at', 'updated_at')
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
            'publication': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }