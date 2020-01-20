from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Clip, Board


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class ClipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clip
        fields = ['name', 'board', 'sound']

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['name', 'cover']