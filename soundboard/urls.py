from django.urls import include, path
from . import views
from rest_framework import routers
import rest_framework.authtoken.views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'clips', views.ClipViewSet)
router.register(r'boards', views.BoardViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', rest_framework.authtoken.views.obtain_auth_token)
]