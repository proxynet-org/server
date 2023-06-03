from rest_framework import serializers
from .models import Zone, Chatroom

class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ('id','coordinates','max_slots','occupied_slots')
        extra_kwargs = {
            'id': {'read_only': True},
        }

class ChatroomSerializer(serializers.ModelSerializer):
    joined = serializers.SerializerMethodField()
    num_people = serializers.SerializerMethodField()
    class Meta:
        model = Chatroom
        fields = ('id','image','name','description','capacity','current_users','lifetime','is_open','is_available','coordinates', 'joined', 'num_people')
        extra_kwargs = {
            'id': {'read_only': True},
            'current_users': {'read_only': True},
            'is_open': {'read_only': True},
            'is_available': {'read_only': True},
            'coordinates': {'read_only': True},
        }
    
    def get_joined(self, obj):
        user = None
        if 'request' in self.context:
            user = self.context['request'].user
        if user in obj.current_users.all():
            return True
        else:
            return False
        
    def get_num_people(self, obj):
        return obj.current_users.count()