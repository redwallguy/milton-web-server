from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Clip, Board, DiscordUser, Alias
from django.core.exceptions import ObjectDoesNotExist
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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
        fields = '__all__'  # auto-generated `id` field must be included for ability to perform instance operations on clips
                            # due to how DRF router urls are auto-generated.

class BoardSerializer(serializers.ModelSerializer):
    clips = ClipSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Board
        fields = ['name', 'cover', 'clips']

class AliasSerializer(serializers.ModelSerializer):
    clip = ClipSerializer(required=False)

    def validate_clip(self, value):
        board = None
        try:
            board = Board.objects.get(name=(value.get('board')))
        except ObjectDoesNotExist:
            raise serializers.ValidationError(detail="Error retrieving board from name")
        try:
            clip = Clip.objects.get(name=value.get('name'), board=board)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(detail="Clip with query parameters could not be found")
        return value

    def create(self, validated_data):
        name = validated_data.get('name')
        clip_data = validated_data.get('clip')
        clip_name = clip_data.get('name')
        board = None
        try:
            board = Board.objects.get(name=clip_data.get('board'))
        except ObjectDoesNotExist:
            raise serializers.ValidationError(detail="Error retrieving board from name")
        try:
            clip = Clip.objects.get(name=clip_name, board=board)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(detail="Clip with query parameters could not be found")
        return Alias.objects.create(name=name, clip=clip)

    class Meta:
        model = Alias
        fields = '__all__'
        

class DiscordUserSerializer(serializers.ModelSerializer):
    intro = ClipSerializer(required=False)

    def validate_intro(self, value):
        board = None
        try:
            board = Board.objects.get(name=value.get('board'))
        except ObjectDoesNotExist:
            raise serializers.ValidationError(detail="Error retrieving board from name")
        try:
            clip = Clip.objects.get(name=value.get('name'), board=board)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(detail="Clip with query parameters could not be found")
        return value

    class Meta:
        model = DiscordUser
        fields = ['user_id', 'role', 'intro']

    def create(self, validated_data):
        user_id = validated_data.get('user_id')
        role = validated_data.get('role', "N")

        intro = validated_data.get('intro')
        clip = None
        if (intro):
            clip_name = intro.get('name')
            board = None
            try:
                board = Board.objects.get(name=intro.get('board'))
            except ObjectDoesNotExist:
                raise serializers.ValidationError(detail="Error retrieving board from name")
            try:
                clip = Clip.objects.get(name=clip_name, board=board)
            except ObjectDoesNotExist:
                raise serializers.ValidationError(detail="Clip with query parameters could not be found")
        return DiscordUser.objects.create(user_id=user_id, role=role, intro=clip)

    def update(self, instance, validated_data):
        user_id = validated_data.get('user_id')
        if user_id is None:
            raise serializers.ValidationError
        intro = validated_data.get('intro')
        clip_name = intro.get('name')
        board = None
        clip = None
        discord_user_instance = None
        try:
            board = Board.objects.get(name=intro.get('board'))
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
        discord_user_instance.save()
        return discord_user_instance
        
        