from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet, give_token,
                    signup)

router = routers.DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
router.register(
    'categories', CategoryViewSet, basename='categories'
)
router.register(
    'genres', GenreViewSet, basename='genres'
)
router.register(
    'users', UserViewSet, basename='users'
)
router.register(
    'titles', TitleViewSet, basename='titles'
)

urlpatterns = [
    path('v1/auth/token/', give_token),
    path('v1/auth/signup/', signup),
    path('v1/', include(router.urls)),
]
