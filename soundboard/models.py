from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from . import validators
from enum import Enum

def clip_upload_handler(instance, filename):
    return 'boards/{0}/clips/{1}/{2}'.format(instance.board.name,instance.name,filename)

def board_upload_handler(instance, filename):
    return 'boards/{0}/cover/{1}'.format(instance.name, filename)

class Board(models.Model):
    name = models.TextField(primary_key=True, max_length=30)
    cover = models.ImageField(upload_to=board_upload_handler)

    def __str__(self):
        return self.name

class Clip(models.Model):
    name = models.TextField(max_length=30)
    board = models.ForeignKey(Board, related_name='clips', on_delete=models.CASCADE)
    sound = models.FileField(validators=[validators.FileTypeValidator(allowed_extensions=['audio/mpeg','audio/ogg'])], upload_to=clip_upload_handler)
    volume = models.IntegerField(default=100, validators=[MinValueValidator(1), MaxValueValidator(100)])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'board'], name='unique_board_clip')
        ]

    def save(self, *args, **kwargs):
        validators.FileTypeValidator(allowed_extensions=['audio/mpeg','audio/ogg']).__call__(self.sound)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name

class Alias(models.Model):
    name = models.TextField(max_length=30)
    clip = models.ForeignKey(Clip, related_name='aliases', on_delete=models.CASCADE)

    def validate_unique(self): # alias name cannot be the same as another alias or clip name on the same board
        if self.__class__.objects.filter(clip__board__name=self.clip.board.name,name=self.name).exists():
            raise ValidationError("Alias with this name already exists on this board.")
        if Clip.objects.filter(board__name=self.clip.board.name,name=self.name).exists():
            raise ValidationError("Clip with this name already exists on this board.")

    def save(self, *args, **kwargs): # validate, then save
        self.validate_unique()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Playlist(models.Model):
    name = models.TextField(max_length=50)
    user = models.ForeignKey(User, related_name='playlists', on_delete=models.CASCADE)
    clips = models.ManyToManyField(Clip, through='PlaylistClip')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name','user'], name='unique_user_playlist')
        ]

    def __str__(self):
        return self.name

class PlaylistClip(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    clip = models.ForeignKey(Clip, on_delete=models.CASCADE)
    next = models.ForeignKey('self', null=True, on_delete=models.SET_NULL) # When inserting, updating, or deleting, modify next reference accordingly

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['playlist','clip'], name='unique_playlist_clip')
        ]
        # TODO make sure that default permissions don't need to be changed for this intermediate class

    def __str__(self):
        return self.playlist.name + ": " + self.clip.name

class DiscordUser(models.Model):

    class DiscordRole(models.TextChoices):
        ADMIN = "A", "Admin"
        MOD = "M", "Moderator"
        BANNED = "B", "Banned"
        NORMAL = "N", "Normal"


    user_id = models.BigIntegerField(primary_key=True)
    role = models.CharField(max_length=15, choices=DiscordRole.choices,default=DiscordRole.NORMAL)
    intro = models.ForeignKey(Clip, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.user_id
