from django.urls import include, path

from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, PostViewSet

router_v1 = DefaultRouter()

router_v1.register(r'posts', PostViewSet, basename='posts')
router_v1.register(
    r'posts/(?P<id>\d+)/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('api/v1/', include(router_v1.urls)),
    path('api/v1/api-auth', include('rest_framework.urls')),
    path('api/v1/api-token-auth/', views.obtain_auth_token),
]
