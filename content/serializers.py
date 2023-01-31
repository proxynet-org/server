from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('user', 'text', 'created_at', 'updated_at', 'location','idUser')
        extra_kwargs = {
            'user': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'location': {'read_only': True},
            'idUser':{'read_only': True}
        }
