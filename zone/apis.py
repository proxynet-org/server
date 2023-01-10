from rest_framework import viewsets
from .models import Zone 
from .serializers import ZoneSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users.models import User

class ZoneViewSet(viewsets.ModelViewset):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer