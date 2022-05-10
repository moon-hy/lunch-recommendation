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
    path('/foods', FoodList.as_view()),
    path('/foods/<int:pk>', FoodDetail.as_view()),
    path('/foods/<int:pk>/reviews', ReviewList.as_view()),
    path('/reviews/<int:pk>', ReviewDetail.as_view()),
    path('/categories', CategoryList.as_view()),
    path('/categories/<int:pk>', CategoryDetail.as_view()),
]
