from random import choices, sample
import datetime

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize
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

class MemoryBasedRecommend(APIView):
    serializer_class    = FoodListSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        df= pd.read_csv('./data/history_test.csv')
        df['date(utc)'] = df['date(utc)'].astype('datetime64')

        # 최근 10일 간의 데이터를 사용
        # 최근 10일 동안 먹지 않았던 점심 중에서 추천을 진행함
        df = df[df['date(utc)'] > np.datetime64(datetime.date.today() - datetime.timedelta(days=10))]

        # 임의로 생성한 데이터이기 때문에 확인이 의미가 없지만 관례상 Train/Test split
        test_df = df.groupby('user').head(3)
        train_df = df[~df.index.isin(test_df.index)]
        train_df['values'] = 1

        # Pivot Table 생성. 더 많이 먹었던 음식엔 높은 값 -> aggfunc = 'sum'
        pivot_table = pd.pivot_table(
            train_df,
            index   ='user',
            columns ='food',
            values  ='values',
            aggfunc ='sum', 
            fill_value=0
        )

        # user_id -> dataframe['user']_index, dataframe['food']_index <-> food_id 매핑
        user_id_to_idx = {user_id: i for i, user_id in enumerate(pivot_table.index)}
        idx_to_food_id = pivot_table.columns
        food_id_to_idx = {food_id: i for i, food_id in enumerate(pivot_table.columns)}


        # 음식 간 유사도를 구함
        sim_food = cosine_similarity(pivot_table.T)

        # pivot_table과 sim_food를 내적하면, 
        # 어떤 음식에 대해 얼마나 유사한 음식을 먹었는가를 수치화 할 수 있음.
        #                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        # 음식 간 유사도: 음식 A와 B를 먹은 사람이 얼마나 비슷한가 = A와 B가 얼마나 유사한가
        #                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        # (피벗 테이블) x (음식 간 유사도): 어떤 사람 1이 어떤 음식 A에 대해 A와 유사한 음식을 많이 먹었다면(유사도가 큰 음식),
        #                                                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        # 상대적으로 높은 수치를 갖게 됨.
        score = pivot_table.dot(sim_food)

        # 수치에서 이미 먹었던 음식은 제외함
        for uid in score.index:
            for ate in train_df[train_df.user==uid].food.values:
                score.loc[uid][food_id_to_idx[ate]] = 0
                
        # 일관된 점수 확인을 위해 정규화
        score_norm = normalize(score, axis=0)
        rank_idx = score_norm.argsort(axis=1)

        # uid에 대한 추천 음식의 id를 저장
        uid = request.user.id
        top_5_idx = rank_idx[user_id_to_idx[uid]][::-1][:5]
        top_5_food_id = [idx_to_food_id[idx] for idx in top_5_idx]

        foods       = Food.objects.filter(id__in=top_5_food_id)
        seriralizer = self.serializer_class(foods, many=True)
        return Response(seriralizer.data, status=HTTP_200_OK)
