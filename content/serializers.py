from typing import Any
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
    image = serializers.SerializerMethodField()


    class Meta:
        model = Publication
        fields = ('id', 'user', 'title', 'text', 'likes', 'dislikes', 'created_at',
                  'updated_at', 'coordinates', 'image', 'num_likes', 'num_dislikes', 'num_comments', 'reaction')
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
        if "user" in self.context:
            user = self.context["user"]
            if user in obj.likes.all():
                return 'LIKE'
            elif user in obj.dislikes.all():
                return 'DISLIKE'
            else:
                return 'NONE'
        else:
            return 'NONE'

    def get_image(self, obj):
        if obj.image:
            base_url = self.context['request'].build_absolute_uri('/')
            base_url = base_url[:-1] # remove last slash
            url = base_url + obj.image.url
            return url
        else:
            return None


class CommentSerializer(serializers.ModelSerializer):
    num_likes = serializers.SerializerMethodField()
    num_dislikes = serializers.SerializerMethodField()
    num_replies = serializers.SerializerMethodField()
    reaction = serializers.SerializerMethodField()



    class Meta:
        model = Comment
        fields = ('id', 'user', 'publication', 'text', 'likes', 'dislikes', 'created_at', 'updated_at',
                   'num_likes', 'num_dislikes', 'is_reply', 'parent_comment' , 'num_replies', 'reaction')   
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
            'publication': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

    def get_num_likes(self, obj):
        return len(obj.likes.all())
    
    def get_num_dislikes(self, obj):
        return len(obj.dislikes.all())

    def get_num_replies(self, obj):
        return len(Comment.objects.filter(parent_comment=obj))
    
    def get_reaction(self, obj):
        if "user" in self.context:
            user = self.context["user"]
            if user in obj.likes.all():
                return 'LIKE'
            elif user in obj.dislikes.all():
                return 'DISLIKE'
            else:
                return 'NONE'
        else:
            return 'NONE'