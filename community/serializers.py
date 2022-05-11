from rest_framework import serializers

from community.models import Post, Comment, Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model       = Category
        fields      = [
            'id', 'name'
        ]

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model       = Comment
        fields      = [
            'id', 'user', 'content', 'created_at'
        ]

class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model       = Comment
        fields      = [
            'content'
        ]
        extra_kwargs= {
            'post'      : {'required': False},
            'content'   : {'required': True}
        }

class PostListSerializer(serializers.ModelSerializer):
    post_id         = serializers.ReadOnlyField(source='id')
    post_title      = serializers.ReadOnlyField(source='title')

    category_id     = serializers.ReadOnlyField(source='category.id')
    category_name   = serializers.ReadOnlyField(source='category.name')
    user_nickname   = serializers.ReadOnlyField(source='user.profile.nickname')
    comments_count  = serializers.ReadOnlyField()

    class Meta:
        model       = Post
        fields      = [
            'post_id', 'post_title', 'category_id', 'category_name', 
            'user_nickname', 'comments_count', 'created_at',
            'category', 'title', 'content'
        ]
        extra_kwargs= {
            'title'     : {'required': True, 'write_only': True},
            'category'  : {'required': True, 'write_only': True},
            'content'   : {'required': True, 'write_only': True}
        }

class PostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model       = Post
        fields      = [
            'category', 'title', 'content',
        ]
        extra_kwargs= {
            'title'     : {'required': True},
            'category'  : {'required': True},
            'content'   : {'required': True}
        }

class PostDetailSerializer(serializers.ModelSerializer):
    nickname        = serializers.ReadOnlyField(source='user.profile.nickname')
    comments        = CommentSerializer('comments', many=True)

    class Meta:
        model       = Post
        fields      = [
            'id', 'user', 'nickname', 'title', 'content', 'created_at', 'comments'
        ]
