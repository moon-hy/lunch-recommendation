from rest_framework import serializers

from food.models import Food, Tag, Review


class ReviewSerializer(serializers.ModelSerializer):
    user            = serializers.ReadOnlyField(source='user.username')
    food            = serializers.ReadOnlyField(source='food.name')

    class Meta:
        model   = Review
        fields  = [
            'id', 'user', 'food', 'content', 'rating', 'created_at' 
        ]

class FoodListSerializer(serializers.ModelSerializer):
    category        = serializers.ReadOnlyField(source='category.name')
    rating_avg      = serializers.ReadOnlyField()
    reviews_count   = serializers.ReadOnlyField()

    class Meta:
        model   = Food
        fields  = [
            'id', 'category', 'name', 'kcal', 'image', 'rating_avg', 'reviews_count'
        ]

class FoodDetailSerializer(serializers.ModelSerializer):
    reviews         = ReviewSerializer(many=True)

    class Meta:
        model   = Food
        fields  = [
            'id', 'name', 'detail', 'kcal', 'image', 'reviews',
        ]
