from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,

    HTTP_400_BAD_REQUEST
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from feature.serializers import (
    CategoryDetailSerializer, 
    CategoryListSerializer, 
    FoodListSerializer, 
    FoodDetailSerializer,
    HistorySerializer,
    ReviewSerializer
)
from feature.models import Category, Food, History, Review
from core.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly


class FoodList(APIView):
    serializer_class    = FoodListSerializer
    permission_classes  = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        operation_id            = '음식 목록 조회',
        operation_description   = '음식 목록을 조회합니다.',
        responses               = {200: openapi.Response('', serializer_class(many=True))}
    )
    def get(self, request):
        foods       = Food.objects.all()
        serializer  = self.serializer_class(foods, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    @swagger_auto_schema(   
        operation_id            = '음식 목록 추가',
        operation_description   = '음식 목록에 데이터를 추가합니다.',
        request_body            = FoodListSerializer,
        responses               = {201: openapi.Response('', serializer_class)}
    )
    def post(self, request):
        serializer  = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class FoodDetail(APIView):
    serializer_class    = FoodDetailSerializer
    permission_classes  = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        operation_id            = '음식 정보 조회',
        operation_description   = '음식 정보를 조회합니다.',
        responses               = {200: openapi.Response('', serializer_class(many=True))}
    )
    def get(self, request, pk):
        food        = Food.objects.get(pk=pk)
        serializer  = self.serializer_class(food)
        return Response(serializer.data, status=HTTP_200_OK)

    @swagger_auto_schema(   
        operation_id            = '음식 정보 수정',
        operation_description   = '음식 정보를 수정합니다.',
        request_body            = serializer_class,
        responses               = {200: openapi.Response('', serializer_class)}
    )   
    def put(self, request, pk):
        food        = Food.objects.get(pk=pk)
        serializer  = self.serializer_class(food, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(   
        operation_id            = '음식 정보 수정',
        operation_description   = '음식 정보를 수정합니다.',
        request_body            = serializer_class,
        responses               = {200: openapi.Response('', serializer_class)}
    )
    def patch(self, request, pk):
        food        = Food.objects.get(pk=pk)
        serializer  = self.serializer_class(food, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(   
        operation_id            = '음식 정보 삭제',
        operation_description   = '음식 정보를 삭제합니다.',
        responses               = {204: openapi.Response('No Content')}
    )
    def delete(self, request, pk):
        food        = Food.objects.get(pk=pk)
        food.delete()
        return Response(status=HTTP_204_NO_CONTENT)

class HistoryList(APIView):
    serializer_class    = HistorySerializer
    permission_classes  = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        operation_id            = '기록 조회',
        operation_description   = '나의 음식 선택 기록을 조회합니다.',
        responses               = {200: openapi.Response('', serializer_class(many=True))}
    )
    def get(self, request):
        histories   = History.objects.filter(user=request.user)
        serializer  = self.serializer_class(histories, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    @swagger_auto_schema(   
        operation_id            = '기록 추가',
        operation_description   = '음식 선택 기록을 추가합니다.',
        responses               = {201: openapi.Response('', serializer_class)}
    )
    def post(self, request):
        serializer  = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class HistoryDetail(APIView):
    serializer_class    = ReviewSerializer
    permission_classes  = (IsAuthenticated, IsOwnerOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    
    def get_object(self, request, pk):
        history     = History.objects.get(pk=pk)
        self.check_object_permissions(request, history)
        return history

    @swagger_auto_schema(   
        operation_id            = '기록 리뷰 조회',
        operation_description   = '해당 기록의 리뷰를 조회합니다.',
        responses               = {201: openapi.Response('', serializer_class)}
    )
    def get(self, request, pk):
        history     = self.get_object(request, pk)
        serializer  = self.serializer_class(history.review)
        return Response(serializer.data, status=HTTP_200_OK)

class FoodReviewList(APIView):
    serializer_class    = ReviewSerializer
    permission_classes  = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        operation_id            = '음식 리뷰 조회',
        operation_description   = '특정 음식의 리뷰를 조회합니다.',
        responses               = {200: openapi.Response('', serializer_class(many=True))}
    )
    def get(self, request, pk):
        reviews     = Review.objects.filter(history__food_id=pk)
        serializer  = self.serializer_class(reviews, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

class ReviewList(APIView):
    serializer_class    = ReviewSerializer
    permission_classes  = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        operation_id            = '리뷰 조회',
        operation_description   = '모든 리뷰를 조회합니다.',
        responses               = {200: openapi.Response('', serializer_class(many=True))}
    )
    def get(self, request):
        reviews     = Review.objects.all()
        serializer  = self.serializer_class(reviews, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    @swagger_auto_schema(   
        operation_id            = '리뷰 등록',
        operation_description   = '리뷰를 등록합니다.',
        request_body            = serializer_class,
        responses               = {201: openapi.Response('', serializer_class)}
    )
    def post(self, request):
        serializer  = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class ReviewDetail(APIView):
    permission_classes  = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication,)

    def get_object(self, request, pk):
        review      = Review.objects.get(pk=pk)
        self.check_object_permissions(request, review)
        return review

    @swagger_auto_schema(
        operation_id            = '리뷰 삭제',
        operation_description   = '리뷰를 삭제합니다.',
        responses               = {204: openapi.Response('No Content')}
    )
    def delete(self, request, pk):
        review       = self.get_object(request, pk)
        review.delete()
        return Response(status=HTTP_204_NO_CONTENT)

class CategoryList(APIView):
    serializer_class    = CategoryListSerializer
    permission_classes  = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        operation_id            = '카테고리 조회',
        operation_description   = '음식의 카테고리 목록을 조회합니다.',
        responses               = {200: openapi.Response('', serializer_class(many=True))}
    )
    def get(self, request):
        categories  = Category.objects.all()
        serializer  = self.serializer_class(categories, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    @swagger_auto_schema(
        operation_id            = '카테고리 추가',
        operation_description   = '음식의 카테고리를 목록에 추가합니다.',
        request_body            = serializer_class,
        responses               = {201: openapi.Response('', serializer_class(many=True))}
    )
    def post(self, request):
        serializer  = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class CategoryDetail(APIView):
    serializer_class    = CategoryDetailSerializer
    permission_classes  = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        operation_id            = '카테고리 상세 조회',
        operation_description   = '음식의 카테고리를 조회합니다.',
        responses               = {200: openapi.Response('', serializer_class(many=True))}
    )
    def get(self, request, pk):
        category    = Category.objects.get(pk=pk)
        serializer  = self.serializer_class(category)
        return Response(serializer.data, status=HTTP_200_OK)
