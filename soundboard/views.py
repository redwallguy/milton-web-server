from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .models import Clip, Board, DiscordUser
from .serializers import UserSerializer, GroupSerializer, ClipSerializer, BoardSerializer, DiscordUserSerializer, DiscordUserIntroUpdateSerializer
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response

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
    API endpoint that allows Discord Users to be viewed or edited #TODO review whether or not viewing ability makes sense privacy-wise
    """
    queryset = DiscordUser.objects.all()
    serializer_class = DiscordUserSerializer
    filterset_fields = ('user_id', 'role')

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except NotFound:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def set_intro(self, request, pk=None):
        user = self.get_object()
        logger.info(request.data)
        serializer = DiscordUserIntroUpdateSerializer(user, data=request.data)
        try:
            serializer.update(instance=user, validated_data=request.data)
            return Response({'status': 'Intro updated'})
        except Exception as e:
            logger.info(e)
            return Response({'error': 'Intro update failed'},
                            status=status.HTTP_400_BAD_REQUEST)