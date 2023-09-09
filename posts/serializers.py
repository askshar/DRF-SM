from rest_framework import serializers

from .models import Post, Comment



class PostSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    post_id = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = [
                'username', 'post_id', 'image', 'caption',
                'description', 'likes', 'total_comments'
            ]
        read_only_fields = ['user', 'likes', 'total_comments']

    def get_username(self, obj):
        return obj.user.username

    def get_likes(self, obj):
        return obj.liked_by.all().count()
    
    def get_post_id(self, obj):
        return obj.id
    
    def get_total_comments(self, obj):
        return obj.comments.all().count()

    # def create(self, validated_data):
    #     request = self.context.get('request')
    #     validated_data['user'] = request.user
    #     return Post.objects.create(**validated_data)


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['username', 'comment']
        read_only_fields = ['post', 'user', 'username']

    def get_username(self, obj):
        return obj.user.username


class PostDetailSerializer(PostSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields + ['comments']
    