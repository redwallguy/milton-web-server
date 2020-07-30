from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .models import Clip, Board, DiscordUser, Alias
from .serializers import UserSerializer, GroupSerializer, ClipSerializer, BoardSerializer, DiscordUserSerializer, AliasSerializer
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

import boto3
from botocore.exceptions import ClientError
import os, re

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
s3_client = boto3.client('s3')

def parseKey(objectURL):
    s3Regex = r"https://" + os.environ.get('AWS_STORAGE_BUCKET_NAME') + r"\.s3\.amazonaws\.com/"
    key = re.sub(s3Regex, "", objectURL)
    logger.info(key)
    return key

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

    @action(detail=True)
    def get_presigned_url(self, request, pk=None):
        serialized_clip = ClipSerializer(self.get_object())
        response = None
        try:
            response = s3_client.generate_presigned_url('get_object',
                                                        Params={'Bucket': os.environ.get('AWS_STORAGE_BUCKET_NAME'),
                                                                'Key': parseKey(serialized_clip.data.get('sound'))})
            logger.info(response)
        except ClientError as e:
            logger.info(e)
        return Response(response)

class BoardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows boards to be viewed or edited.
    """
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    filterset_fields = ('name',)

class AliasViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows aliases to be viewed or edited.
    """
    queryset = Alias.objects.all()
    serializer_class = AliasSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class DiscordUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Discord Users to be viewed or edited
    """

    permission_classes=[IsAdminUser]
    
    queryset = DiscordUser.objects.all()
    serializer_class = DiscordUserSerializer
    filterset_fields = ('user_id', 'role')

    def create(self, request):
        serializer = self.get_serializer(data=request.data, partial=True) # This method must be overwritten with partial=True to prevent validation errors
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)