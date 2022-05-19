from random import choices, sample
import datetime

from django.db.models import Count
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

from feature.models import Food, History
from feature.serializers import FoodDetailSerializer, FoodListSerializer

class RandomRecommend(APIView):
    serializer_class    = FoodListSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(   
        operation_id            = '음식 추천 - 랜덤',
        operation_description   = '랜덤으로 음식을 추천합니다.',
        responses               = {200: openapi.Response('', FoodListSerializer)}
    )
    def get(self, request):
        foods       = Food.objects.all()
        counts_foods= foods.count()
        foods_chosen= sample(list(foods), k=min(10, counts_foods))
        serializer  = self.serializer_class(foods_chosen, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class YesterdayPopularRecommend(APIView):
    serializer_class    = FoodListSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(   
        operation_id            = '음식 추천 - 인기',
        operation_description   = '다른 사용자들이 어제 가장 많이 먹은 음식을 추천합니다.',
        responses               = {200: openapi.Response('', FoodListSerializer)}
    )
    def get(self, request):
        yesterday   = datetime.date.today() - datetime.timedelta(days=1)

        histories   = History.objects.all().values(
            'food'
        ).filter(
            created_at__gte=yesterday
        ).annotate(
            count=Count('id')
        ).order_by('-count')
        
        foods       = []
        idx         = 0
        
        while len(foods)<10 and idx<len(histories):
            food_id = histories[idx]['food']
            try:
                foods.append(Food.objects.get(pk=food_id))
            except:
                pass
            idx += 1

        serializer  = self.serializer_class(foods, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
