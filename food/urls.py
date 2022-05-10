from django.urls import path, include

from food.views import (
    FoodList,
    FoodDetail,
    
    ReviewDetail,
    ReviewList,

    CategoryList,
    CategoryDetail,
)


urlpatterns = [
    path('', FoodList.as_view()),
    path('/<int:pk>', FoodDetail.as_view()),
    path('/<int:pk>/reviews', ReviewList.as_view()),
    path('/reviews/<int:pk>', ReviewDetail.as_view()),
    path('/categories', CategoryList.as_view()),
    path('/categories/<int:pk>', CategoryDetail.as_view()),
]
