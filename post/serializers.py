from rest_framework import serializers

from post.models import Post, Comment


class PostCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model       = Comment
        fields      = [
            'id', 'user', 'content', 'created_at'
        ]

class PostListSerializer(serializers.ModelSerializer):
    user            = serializers.ReadOnlyField(source='user.username')
    comments_count  = serializers.ReadOnlyField()

    class Meta:
        model       = Post
        fields      = [
            'id', 'user', 'title', 'content', 'comments_count', 'created_at'
        ]

class PostDetailSerializer(serializers.ModelSerializer):
    user            = serializers.ReadOnlyField(source='user.username')
    comments        = PostCommentSerializer('comments', many=True)

    class Meta:
        model       = Post
        fields      = [
            'id', 'user', 'title', 'content', 'created_at', 'comments'
        ]

class CommentSerializer(serializers.ModelSerializer):
    user            = serializers.ReadOnlyField(source='user.username')
    post            = serializers.ReadOnlyField(source='post.title')

    class Meta:
        model       = Comment
        fields      = [
            'id', 'user', 'post', 'content', 'created_at'
        ]
