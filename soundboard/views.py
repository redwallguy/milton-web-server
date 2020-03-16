from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .models import Clip, Board
from .serializers import UserSerializer, GroupSerializer, ClipSerializer, BoardSerializer


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
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Clip.objects.all()
    serializer_class = ClipSerializer
    filterset_fields=('name', 'board')

class BoardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    filterset_fields = ('name',)