from django.test import TestCase, TransactionTestCase
import soundboard.models as models
from django.core.files import File
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError
import pytest

pytestmark = pytest.mark.django_db(transaction=True)

# TODO find out how to resolve differences between pytest and unittest to properly test django-cleanup
# For now, manually put up/tear down parents each test

class BoardTestCase(TransactionTestCase):

    def test_board(self):
        board = models.Board(name='test', cover=File(name='pearl',file=open('/mnt/c/Users/conta/Coding/soundboard/milton_web_server/soundboard/tests/media/pearl.jpg','rb')))
        board.save()
        assert board.cover.url is not None
        assert board.name == 'test'
        board.delete()
        print("Board deleted")
        assert default_storage.exists(board.cover.url) == False

    def test_clip(self):
        board = models.Board(name='test', cover=File(name='pearl',file=open('/mnt/c/Users/conta/Coding/soundboard/milton_web_server/soundboard/tests/media/pearl.jpg','rb')))
        board.save()
        clip = models.Clip(name='test', board=board, sound=File(name='dunk',file=open(
            '/mnt/c/Users/conta/Coding/soundboard/milton_web_server/soundboard/tests/media/dunk_hb.mp3','rb')))
        clip.save()
        assert clip.sound.url is not None
        assert clip.name == 'test'
        board.delete()
        print("Board deleted")
        assert default_storage.exists(clip.sound.url) == False

    def test_alias_clip_name_conflict(self):
        board = models.Board(name='test', cover=File(name='pearl',file=open('/mnt/c/Users/conta/Coding/soundboard/milton_web_server/soundboard/tests/media/pearl.jpg','rb')))
        board.save()
        clip = models.Clip(name='test', board=board, sound=File(name='dunk',file=open(
            '/mnt/c/Users/conta/Coding/soundboard/milton_web_server/soundboard/tests/media/dunk_hb.mp3','rb')))
        clip.save()
        alias = models.Alias(name='test', clip=clip)
        with pytest.raises(ValidationError):
            alias.save()
        board.delete()
        print("Board deleted")

    def test_alias_board_uniqueness_conflict(self):
        board = models.Board(name='test', cover=File(name='pearl',file=open('/mnt/c/Users/conta/Coding/soundboard/milton_web_server/soundboard/tests/media/pearl.jpg','rb')))
        board.save()
        clip = models.Clip(name='test', board=board, sound=File(name='dunk',file=open(
            '/mnt/c/Users/conta/Coding/soundboard/milton_web_server/soundboard/tests/media/dunk_hb.mp3','rb')))
        clip.save()
        clip_to_conflict = models.Clip(name='test_conflict', board=board, sound=File(name='dunk',file=open(
            '/mnt/c/Users/conta/Coding/soundboard/milton_web_server/soundboard/tests/media/dunk_hb.mp3','rb')))
        clip_to_conflict.save()
        alias = models.Alias(name='test_alias', clip=clip)
        alias.save()
        alias_to_conflict = models.Alias(name='test_alias', clip=clip_to_conflict)
        with pytest.raises(ValidationError):
            alias_to_conflict.save()
        board.delete()
        print("Board deleted")
