from rest_framework import serializers

from community.models import Post, Comment, Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model       = Category
        fields      = [
            'id', 'name'
        ]

class CommentSerializer(serializers.ModelSerializer):
    post_id         = serializers.PrimaryKeyRelatedField(
        queryset    = Post.objects.all(),
        source      = 'post',
    )

    comment_id         = serializers.ReadOnlyField(
        source      = 'id',
    )

    nickname        = serializers.ReadOnlyField(
        source      = 'user.profile.nickname'
    )

    class Meta:
        model       = Comment
        fields      = [
            'post_id', 'comment_id', 
            'nickname', 'content', 'created_at'
        ]
        extra_kwargs= {
            'created_at': {'read_only': True},
            'post_id'   : {'required': True, 'write_only': True},
            'content'   : {'required': True},
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

class PostDetailSerializer(serializers.ModelSerializer):
    nickname        = serializers.ReadOnlyField(source='user.profile.nickname')
    comments        = CommentSerializer('comments', many=True)

    class Meta:
        model       = Post
        fields      = [
            'id', 'user', 'nickname', 'title', 'content', 'created_at', 'comments'
        ]
