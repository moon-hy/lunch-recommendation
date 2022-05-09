from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,

    HTTP_400_BAD_REQUEST
)

from food.serializers import FoodListSerializer, FoodDetailSerializer, ReviewListSerializer
from food.models import Food, Review


class FoodList(APIView):
    serializer_class= FoodListSerializer

    def get(self, request):
        foods       = Food.objects.all()
        serializer  = self.serializer_class(foods, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request):
        serializer  = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class FoodDetail(APIView):
    serializer_class= FoodDetailSerializer

    def get(self, request, pk):
        food        = Food.objects.get(pk=pk)
        serializer  = self.serializer_class(food)
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, pk):
        food        = Food.objects.get(pk=pk)
        serializer  = self.serializer_class(food, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        food        = Food.objects.get(pk=pk)
        serializer  = self.serializer_class(food, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        food        = Food.objects.get(pk=pk)
        food.delete()
        return Response(status=HTTP_204_NO_CONTENT)

class ReviewList(APIView):
    serializer_class= ReviewListSerializer

    def get(self, request, pk):
        reviews     = Review.objects.filter(food=pk)
        serializer  = self.serializer_class(reviews, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request, pk):
        serializer  = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)