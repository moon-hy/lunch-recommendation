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


User = get_user_model()

class RandomRecommend(APIView):
    serializer_class    = FoodListSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny, )

    @swagger_auto_schema(   
        operation_id            = '음식 추천 - 랜덤',
        operation_description   = '랜덤으로 음식을 추천합니다.',
        responses               = {200: openapi.Response('', FoodListSerializer)}
    )
    def get(self, request):
        foods       = Food.objects.all()
        counts_foods= foods.count()
        foods_chosen= sample(list(foods), k=min(5, counts_foods))
        serializer  = self.serializer_class(foods_chosen, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class YesterdayPopularRecommend(APIView):
    serializer_class    = FoodListSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny, )

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

class InterestPopularRecommend(APIView):
    serializer_class    = FoodListSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(   
        operation_id            = '음식 추천 - 선호대분류 기반',
        operation_description   = '선택한 선호 대분류에서 가장 인기있는 음식을 추천합니다.',
        responses               = {200: openapi.Response('', FoodListSerializer)}
    )
    def get(self, request):
        last_month  = datetime.date.today() - datetime.timedelta(days=30)
        
        histories   = History.objects.select_related(
            'food__category'
        ).all().values(
            'food'
        ).filter(
            food__category =request.user.profile.interest_in
        ).filter(
            created_at__gte=last_month
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

class InterestUserRecommend(APIView):
    serializer_class    = FoodListSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(   
        operation_id            = '음식 추천 - 유저/선호대분류 기반',
        operation_description   = '같은 선호대분류를 선택한 유저들의 인기 음식을 추천합니다.',
        responses               = {200: openapi.Response('', FoodListSerializer)}
    )
    def get(self, request):
        users       = User.objects.select_related(
            'profile__interest_in'
        ).filter(
            profile__interest_in=request.user.profile.interest_in
        )

        histories   = History.objects.values(
            'food'
        ).filter(
            user__in= users
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
