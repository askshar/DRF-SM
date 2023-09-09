from rest_framework import views, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins, generics

from .models import Post, Comment
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer
from .permissions import PostOwnerOrReadOnly, CommentOwnerOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, PostOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'post_comment':
            self.serializer_class = CommentSerializer
            return self.serializer_class
        if self.action == 'retrieve':
            self.serializer_class = PostDetailSerializer
            return self.serializer_class
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['GET'])
    def user_posts(self, request):
        """
        :param request:
        :return all posts of current user (to show in profile section).
        """
        user = request.user
        user_posts = Post.objects.filter(user=user)
        serializer = self.get_serializer(user_posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def post_like(self, request, pk=None):
        user = request.user
        obj = self.get_object()
        if user in obj.liked_by.all():
            obj.liked_by.remove(user)
            return Response(status=status.HTTP_200_OK)
        obj.liked_by.add(user)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def post_comment(self, request, pk=None):
        comment = request.POST.get('comment')
        if not comment:
            return Response(
                {'Comment': 'required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = CommentSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, post=self.get_object())
        return Response({'Success': 'Comment added.'}, status=status.HTTP_200_OK)
    

class CommentUpdateDeleteView(
        generics.UpdateAPIView,
        generics.DestroyAPIView
    ):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [
                IsAuthenticated,
                CommentOwnerOrReadOnly
            ]
