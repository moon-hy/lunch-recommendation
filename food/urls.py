from django.urls import path, include

from food.views import (
    FoodList,
    FoodDetail,

    ReviewList
)


urlpatterns = [
    path('', FoodList.as_view()),
    path('/<int:pk>', FoodDetail.as_view()),
    path('/<int:pk>/reviews', ReviewList.as_view())
]
