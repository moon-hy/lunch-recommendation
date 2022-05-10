from random import randint

from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,

    HTTP_400_BAD_REQUEST,
)

from food.models import Food
from food.serializers import FoodDetailSerializer, FoodListSerializer

class RandomRecommend(APIView):
    serializer_class    = FoodDetailSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        foods       = Food.objects.all()
        counts_foods= foods.count()
        food        = foods[randint(0, counts_foods-1)]
        serializer  = self.serializer_class(food)
        return Response(serializer.data, status=HTTP_200_OK)
