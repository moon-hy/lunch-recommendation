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
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from feature.models import Food
from feature.serializers import FoodDetailSerializer, FoodListSerializer

class RandomRecommend(APIView):
    serializer_class    = FoodDetailSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(   
        operation_id            = '음식 랜덤 추천',
        operation_description   = '랜덤으로 음식을 추천합니다.',
        responses               = {200: openapi.Response('', FoodDetailSerializer)}
    )
    def get(self, request):
        foods       = Food.objects.all()
        counts_foods= foods.count()
        food        = foods[randint(0, counts_foods-1)]
        serializer  = self.serializer_class(food)
        return Response(serializer.data, status=HTTP_200_OK)
