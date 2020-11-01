from django.urls import include, path, re_path
from . import apiviews, views
from rest_framework import routers
import rest_framework.authtoken.views

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.info("Before router")

router = routers.DefaultRouter()
router.register(r'users', apiviews.UserViewSet)
router.register(r'groups', apiviews.GroupViewSet)
router.register(r'clips', apiviews.ClipViewSet)
router.register(r'boards', apiviews.BoardViewSet)
router.register(r'discord-users', apiviews.DiscordUserViewSet)
router.register(r'aliases', apiviews.AliasViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    re_path(r'^boards/(?P<board_name>\w{1,30})/$', views.clips, name='clips'),
    path('api/', include(router.urls)), # Browsable API paths
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')), # DRF Authentication paths
    path('api-token-auth/', rest_framework.authtoken.views.obtain_auth_token), # Path for generating token
    path('', views.boards, name='boards'),
]

logger.info("After url")