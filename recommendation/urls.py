from django.urls import path

from recommendation.views import (
    RandomRecommend
)


urlpatterns = [
    path('random-recommend', RandomRecommend.as_view())
]
