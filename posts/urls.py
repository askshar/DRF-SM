from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import PostViewSet, CommentUpdateDeleteView

router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')
# print("URLS: ", router.urls)

urlpatterns = [
    path('', include(router.urls)),
    path('comment/<int:pk>/', CommentUpdateDeleteView.as_view()),
]
