from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Board(models.Model):
    name = models.TextField(primary_key=True, max_length=30)
    #cover = models.FileField(name="Cover",) #TODO use python-magic mime=True, use s3
    #Validate file-type on form and on save

    def __str__(self):
        return self.name

class Clip(models.Model):
    name = models.TextField(max_length=30)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    #sound = models.FileField(name="sound") # TODO storage

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'board'], name='unique_board_clip')
        ]


    def __str__(self):
        return self.name

class Alias(models.Model):
    name = models.TextField(max_length=30)
    clip = models.ForeignKey(Clip, on_delete=models.CASCADE)

    def validate_unique(self):
        if self.__class__.objects.filter(clip__board__name=self.clip.board.name,name=self.name).exists():
            raise ValidationError("Alias with this name already exists on this board.")
        if Clip.objects.filter(board__name=self.clip.board.name,name=self.name).exists():
            raise ValidationError("Clip with this name already exists on this board.")

    def save(self, *args, **kwargs):
        self.validate_unique()
        super(Alias, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Playlist(models.Model):
    name = models.TextField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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

    def __str__(self):
        return self.playlist.name + ": " + self.clip.name
