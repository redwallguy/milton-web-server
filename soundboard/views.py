from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .models import Clip, Board, DiscordUser
from .serializers import UserSerializer, GroupSerializer, ClipSerializer, BoardSerializer, DiscordUserSerializer
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

import logging

logger = logging.getLogger(__name__)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class ClipViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows clips to be viewed or edited.
    """
    queryset = Clip.objects.all()
    serializer_class = ClipSerializer
    filterset_fields=('name', 'board')

class BoardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows boards to be viewed or edited.
    """
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    filterset_fields = ('name',)

class DiscordUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Discord Users to be viewed or edited
    """

    permission_classes=[IsAdminUser]
    
    queryset = DiscordUser.objects.all()
    serializer_class = DiscordUserSerializer
    filterset_fields = ('user_id', 'role')