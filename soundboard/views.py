from django.shortcuts import render
from rest_framework import status
from soundboard.models import Board, Clip

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def boards(request):
    board_list = Board.objects.all()
    return render(request, "soundboard/boards.html", context={"boards": board_list})

def clips(request, board_name):
    board = None
    try:
        board = Board.objects.get(name=board_name)
    except:
        return render("404", status=status.HTTP_404_NOT_FOUND)
    clip_set = board.clip_set.all()
    aliases = {}
    for clip in clip_set:
        aliases[clip.name] = clip.alias_set.all()
    return render(request, "soundboard/clips.html", context={
        "board": board,
        "clips": clip_set,
        "aliases": aliases
    })