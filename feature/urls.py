from django.urls import path, include

from feature.views import (
    FoodList,
    FoodDetail,
    FoodRanking,
    FoodReviewList,

    HistoryList,
    HistoryDetail,
    
    ReviewList,
    ReviewDetail,

    CategoryList,
    CategoryDetail,
)


urlpatterns = [
    path('foods', FoodList.as_view()),
    path('foods/<int:pk>', FoodDetail.as_view()),
    path('foods/<int:pk>/reviews', FoodReviewList.as_view()),
    
    path('histories', HistoryList.as_view()),
    path('histories/<int:pk>', HistoryDetail.as_view()),

    path('reviews', ReviewList.as_view()),
    path('reviews/<int:pk>', ReviewDetail.as_view()),

    path('categories', CategoryList.as_view()),
    path('categories/<int:pk>', CategoryDetail.as_view()),

    path('ranking/foods', FoodRanking.as_view())
]
