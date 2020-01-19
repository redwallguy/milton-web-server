from django.test import TestCase, TransactionTestCase
import soundboard.models as models
from django.core.files import File
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
import pytest, os
from django.contrib.auth.models import User

media_location = os.environ.get("TEST_MEDIA")

pytestmark = pytest.mark.django_db(transaction=True)

# TODO find out how to resolve differences between pytest and unittest to properly test django-cleanup
# For now, manually put up/tear down file-storing parents each test

class BoardTestCase(TransactionTestCase):

    def test_board_cleanup(self):
        board = models.Board(name='test', cover=File(name='pearl',file=open(media_location + 'pearl.jpg','rb')))
        board.save()
        assert board.cover.url is not None
        assert board.name == 'test'
        board.delete()
        assert default_storage.exists(board.cover.url) == False

    def test_clip_cleanup(self):
        board = models.Board(name='test', cover=File(name='pearl',file=open(media_location + 'pearl.jpg','rb')))
        board.save()
        clip = models.Clip(name='test', board=board, sound=File(name='dunk',file=open(
            media_location + 'dunk_hb.mp3','rb')))
        clip.save()
        assert clip.sound.url is not None
        assert clip.name == 'test'
        board.delete()
        assert default_storage.exists(clip.sound.url) == False

    def test_alias_clip_name_conflict(self):
        board = models.Board(name='test', cover=File(name='pearl',file=open(media_location + 'pearl.jpg','rb')))
        board.save()
        clip = models.Clip(name='test', board=board, sound=File(name='dunk',file=open(
            media_location + 'dunk_hb.mp3','rb')))
        clip.save()
        alias = models.Alias(name='test', clip=clip)
        with pytest.raises(ValidationError):
            alias.save()
        board.delete()

    def test_alias_board_uniqueness_conflict(self):
        board = models.Board(name='test', cover=File(name='pearl',file=open(media_location + 'pearl.jpg','rb')))
        board.save()
        clip = models.Clip(name='test', board=board, sound=File(name='dunk',file=open(
            media_location + 'dunk_hb.mp3','rb')))
        clip.save()
        clip_to_conflict = models.Clip(name='test_conflict', board=board, sound=File(name='dunk',file=open(
            media_location + 'dunk_hb.mp3','rb')))
        clip_to_conflict.save()
        alias = models.Alias(name='test_alias', clip=clip)
        alias.save()
        alias_to_conflict = models.Alias(name='test_alias', clip=clip_to_conflict)
        with pytest.raises(ValidationError):
            alias_to_conflict.save()
        board.delete()

    def test_playlist_user_name_uniqueness(self):
        user = User(username="test", password="test")
        user.save()
        playlist = models.Playlist(name="test",user=user)
        playlist.save()
        playlist_to_conflict = models.Playlist(name="test",user=user)
        with pytest.raises(IntegrityError):
            playlist_to_conflict.save()

    def test_playlist_clip_uniqueness(self):
        user = User(username="test", password="test")
        user.save()
        playlist = models.Playlist(name="test",user=user)
        playlist.save()
        board = models.Board(name='test', cover=File(name='pearl',file=open(media_location + 'pearl.jpg','rb')))
        board.save()
        clip = models.Clip(name='test', board=board, sound=File(name='dunk',file=open(
            media_location + 'dunk_hb.mp3','rb')))
        clip.save()
        playlist_clip = models.PlaylistClip(clip=clip, playlist=playlist)
        playlist_clip.save()
        playlist_clip_to_conflict = models.PlaylistClip(clip=clip, playlist=playlist)
        with pytest.raises(IntegrityError):
            playlist_clip_to_conflict.save()
        board.delete()

    def test_playlist_clip_next_null(self):
        user = User(username="test", password="test")
        user.save()
        playlist = models.Playlist(name="test",user=user)
        playlist.save()
        board = models.Board(name='test', cover=File(name='pearl',file=open(media_location + 'pearl.jpg','rb')))
        board.save()
        clip = models.Clip(name='test', board=board, sound=File(name='dunk',file=open(
            media_location + 'dunk_hb.mp3','rb')))
        clip.save()
        playlist_clip = models.PlaylistClip(clip=clip, playlist=playlist,next=None)
        playlist_clip.save()
        board.delete()

    def test_playlist_clip_next(self):
        user = User(username="test", password="test")
        user.save()
        playlist = models.Playlist(name="test",user=user)
        playlist.save()
        board = models.Board(name='test', cover=File(name='pearl',file=open(media_location + 'pearl.jpg','rb')))
        board.save()
        clip = models.Clip(name='test', board=board, sound=File(name='dunk',file=open(
            media_location + 'dunk_hb.mp3','rb')))
        clip.save()
        clip_next = models.Clip(name='test_next', board=board, sound=File(name='dunk',file=open(
            media_location + 'dunk_hb.mp3','rb')))
        clip_next.save()
        playlist_clip_next = models.PlaylistClip(clip=clip_next,playlist=playlist,next=None)
        playlist_clip_next.save()
        playlist_clip = models.PlaylistClip(clip=clip, playlist=playlist,next=playlist_clip_next)
        playlist_clip.save()
        board.delete()

    def test_playlist_clip_next_deleted(self):
        user = User(username="test", password="test")
        user.save()
        playlist = models.Playlist(name="test",user=user)
        playlist.save()
        board = models.Board(name='test', cover=File(name='pearl',file=open(media_location + 'pearl.jpg','rb')))
        board.save()
        clip = models.Clip(name='test', board=board, sound=File(name='dunk',file=open(
            media_location + 'dunk_hb.mp3','rb')))
        clip.save()
        clip_next = models.Clip(name='test_next', board=board, sound=File(name='dunk',file=open(
            media_location + 'dunk_hb.mp3','rb')))
        clip_next.save()
        playlist_clip_next = models.PlaylistClip(clip=clip_next,playlist=playlist,next=None)
        playlist_clip_next.save()
        playlist_clip = models.PlaylistClip(clip=clip, playlist=playlist,next=playlist_clip_next)
        playlist_clip.save()
        playlist_clip_next.delete()
        playlist_clip_new_instance = models.PlaylistClip.objects.get(clip=clip,playlist=playlist) # Requery because Django model instances persist even after deletion in database
        assert playlist_clip_new_instance.next is None
        board.delete()