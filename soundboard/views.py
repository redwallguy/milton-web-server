from django.shortcuts import render
from rest_framework import status
from soundboard.models import Board, Clip
from django.core.exceptions import ObjectDoesNotExist

import boto3
from botocore.exceptions import ClientError
import logging, os, re

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
s3_client = boto3.client('s3')

def parseKey(objectURL):
    s3Regex = r"https://" + os.environ.get('AWS_STORAGE_BUCKET_NAME') + r"\.s3\.amazonaws\.com/"
    key = re.sub(s3Regex, "", objectURL)
    logger.info(key)
    return key

def get_presigned_covers(): # Returns list of objects with board name and presigned cover url
    cover_presigned_list = []
    for board in Board.objects.all():
        response = None
        try:
            response = s3_client.generate_presigned_url('get_object',
                                                        Params={'Bucket': os.environ.get('AWS_STORAGEBUCKET_NAME'),
                                                                'Key': parseKey(board.cover.name)})
        except ClientError as e:
            logger.info(e)
        board_object = {
            "name": board.name,
            "cover": response
        }
        cover_presigned_list.append(board_object)

def get_presigned_url_dict(board_name):
    board = None
    try:
        board = Board.objects.get(name=board_name)
    except ObjectDoesNotExist:
        return None

    board_presigned_dict = {}
    response = None

    try: # Board cover url
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': os.environ.get('AWS_STORAGEBUCKET_NAME'),
                                                            'Key': parseKey(board.cover.name)})
    except ClientError as e:
        logger.info(e)
    board_presigned_dict['cover'] = response

    board_presigned_dict['clips'] = {}
    for clip in board.clips.all(): #clip urls
        response = None
        try:
            response = s3_client.generate_presigned_url('get_object',
                                                        Params={'Bucket': os.environ.get('AWS_STORAGEBUCKET_NAME'),
                                                                'Key': parseKey(clip.sound)})
        except ClientError as e:
            logger.info(e)
        board_presigned_dict['clips'][clip.name] = response

def boards(request):
    board_list = get_presigned_cover_list()
    return render(request, "soundboard/boards.html", context={"boards": board_list})

def clips(request, board_name):

    board = None
    try:
        board = Board.objects.get(name=board_name)
    except:
        return render("404", status=status.HTTP_404_NOT_FOUND)
    clip_set = board.clip_set.all()
    presigned_urls = get_presigned_url_dict(board_name)
    aliases = {}
    for clip in clip_set:
        aliases[clip.name] = clip.alias_set.all()
    return render(request, "soundboard/clips.html", context={
        "board": board,
        "clips": clip_set,
        "aliases": aliases,
        "presigned_urls": presigned_urls
    })