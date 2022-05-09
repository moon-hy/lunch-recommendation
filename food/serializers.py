from rest_framework import serializers

from food.models import Food, Tag, Review


class ReviewListSerializer(serializers.ModelSerializer):
    user        = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model   = Review
        fields  = [
            'id', 'user', 'food', 'content', 'rating', 
        ]

class ReviewDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model   = Review
        fields  = [
            'id', 
        ]

class FoodListSerializer(serializers.ModelSerializer):
    rating_avg  = serializers.ReadOnlyField()

    class Meta:
        model   = Food
        fields  = [
            'id', 'name', 'detail', 'kcal', 'image', 'rating_avg'
        ]

class FoodDetailSerializer(serializers.ModelSerializer):
    reviews     = ReviewListSerializer(many=True)

    class Meta:
        model   = Food
        fields  = [
            'id', 'name', 'detail', 'kcal', 'image', 'reviews',
        ]
