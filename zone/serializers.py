from rest_framework import serializers
from .models import Zone

class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ('id','coordinates','max_slots','occupied_slots')
        extra_kwargs = {
            'id': {'read_only': True},
        }