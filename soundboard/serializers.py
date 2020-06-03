from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Clip, Board, DiscordUser
from django.core.exceptions import ObjectDoesNotExist
import logging

logger = logging.getLogger(__name__)


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

class ClipReadOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Clip
        fields = ['name', 'board', 'sound']
        read_only_fields = ['name', 'board', 'sound']

class BoardSerializer(serializers.ModelSerializer):
    clips = ClipSerializer(many=True)

    class Meta:
        model = Board
        fields = ['name', 'cover', 'clips']

class DiscordUserSerializer(serializers.ModelSerializer):
    intro = ClipReadOnlySerializer()

    class Meta:
        model = DiscordUser
        fields = ['user_id', 'role', 'intro']

class DiscordUserIntroUpdateSerializer(serializers.ModelSerializer):
    intro = ClipSerializer()

    class Meta:
        model = DiscordUser
        fields = ['user_id', 'role', 'intro']

    def update(self, instance, validated_data):
        logger.info(validated_data)
        logger.info("update")
        user_id = validated_data.get('user_id', None)
        if user_id is None:
            raise serializers.ValidationError
        intro = validated_data.get('intro', None)
        clip_name = intro.get('name', None)
        board = None
        clip = None
        discord_user_instance = None
        try:
            board = Board.objects.get(name=intro.get('board', None))
        except ObjectDoesNotExist:
            raise serializers.ValidationError(detail="Error retrieving board from name")
        try:
            clip = Clip.objects.get(name=clip_name, board=board)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(detail="Clip with query parameters could not be found")
        try:
            discord_user_instance = DiscordUser.objects.get(user_id=user_id)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(detail="No user with id found")
        discord_user_instance.intro = clip
        logger.info(discord_user_instance)
        discord_user_instance.save()
        return discord_user_instance

        
        
        