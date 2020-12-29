from django.urls import include, path
from . import apiviews, views
from rest_framework import routers
import rest_framework.authtoken.views

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

router = routers.DefaultRouter()
router.register(r'clips', apiviews.ClipViewSet)
router.register(r'boards', apiviews.BoardViewSet)
router.register(r'discord-users', apiviews.DiscordUserViewSet)
router.register(r'aliases', apiviews.AliasViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', views.boards),
    path('boards/<str:board>/$', views.clips),
    path('api/', include(router.urls)), # Browsable API paths
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')), # DRF Authentication paths
    path('api-token-auth/', rest_framework.authtoken.views.obtain_auth_token), # Path for generating token
]