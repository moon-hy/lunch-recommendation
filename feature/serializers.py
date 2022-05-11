from rest_framework import serializers

from feature.models import Category, Food, History, Review


class ReviewSerializer(serializers.ModelSerializer):
    nickname        = serializers.ReadOnlyField(source='user.profile.nickname')
    food_name       = serializers.ReadOnlyField(source='history.food.name')

    class Meta:
        model   = Review
        fields  = [
            'id', 'nickname', 'food_name', 'content', 'rating', 'created_at' 
        ]

class ReviewCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model   = Review
        fields  = [
            'id', 'rating', 'content', 'created_at' 
        ]
        extra_kwargs = {
            'rating': {'required': True},
            'content': {'required': False},
        }

    def validate(self, attrs):
        if not (0 <= attrs['rating'] <= 5):
            raise serializers.ValidationError('Invalid rating.')
        return attrs

class FoodListSerializer(serializers.ModelSerializer):
    food_id         = serializers.ReadOnlyField(source='id')
    food_name       = serializers.ReadOnlyField(source='name')
    category_id     = serializers.ReadOnlyField(source='category.id')
    category_name   = serializers.ReadOnlyField(source='category.name')
    rating_avg      = serializers.ReadOnlyField()
    reviews_count   = serializers.ReadOnlyField()

    class Meta:
        model   = Food
        fields  = [
            'food_id', 'food_name', 
            'category_id', 'category_name', 'image', 
            'reviews_count', 'rating_avg',

            'category', 'name', 'kcal', 'image',
        ]
        extra_kwargs = {
            'name'      : {'required': True, 'write_only': True},
            'category'  : {'required': True, 'write_only': True},
            'kcal'      : {'required': False, 'write_only': True},
            'image'     : {'required': False, 'write_only': True}
        }

class FoodCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model   = Food
        fields  = [
            'category', 'name', 'kcal', 'image'
        ]
        extra_kwargs = {
            'name'      : {'required': True},
            'category'  : {'required': True},
            'kcal'      : {'required': False},
            'image'     : {'required': False}
        }

class FoodDetailSerializer(serializers.ModelSerializer):
    food_id         = serializers.ReadOnlyField(source='id')
    food_name       = serializers.ReadOnlyField(source='name')
    category_id     = serializers.ReadOnlyField(source='category.id')
    category_name   = serializers.ReadOnlyField(source='category.name')
    rating_avg      = serializers.ReadOnlyField()
    reviews         = ReviewSerializer(many=True)

    class Meta:
        model   = Food
        fields  = [
            'food_id', 'food_name', 'category_id', 'category_name', 
            'detail', 'kcal', 'image', 'reviews', 'rating_avg'
        ]

class HistoryListSerializer(serializers.ModelSerializer):
    history_id  = serializers.ReadOnlyField(source='id')
    food_id     = serializers.ReadOnlyField(source='food.id')
    food_name   = serializers.ReadOnlyField(source='food.name')

    class Meta:
        model   = History
        fields  = [
            'history_id', 'food_id', 'food_name', 'created_at', 'is_reviewed'
        ]

class CategoryListSerializer(serializers.ModelSerializer):
    category_id = serializers.ReadOnlyField(source='id')
    category_name = serializers.ReadOnlyField(source='name')
    category_count_foods = serializers.ReadOnlyField(source='count_foods')

    class Meta:
        model   = Category
        fields  = [
            'category_id', 'category_name', 'category_count_foods', 'name',
        ]
        extra_kwargs= {
            'name': {'write_only': True}
        }

class CategoryDetailSerializer(serializers.ModelSerializer):
    foods       = FoodListSerializer(many=True)

    class Meta:
        model   = Category
        fields  = [
            'id', 'name', 'foods'
        ]
