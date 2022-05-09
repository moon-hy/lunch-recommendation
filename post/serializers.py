from rest_framework import serializers

from post.models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    user            = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model       = Post
        fields      = [
            'id', 'user', 'title', 'content', 'created_at'
        ]

class PostDetailSerializer(serializers.ModelSerializer):
    user            = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model       = Post
        fields      = [
            'id', 'user', 'title', 'content', 'created_at'
        ]

class CommentSerializer(serializers.ModelSerializer):
    pass