from django.urls import path

from recommendation.views import (
    RandomRecommend,
    YesterdayPopularRecommend
)


urlpatterns = [
    path('random', RandomRecommend.as_view()),
    path('yesterday-popular', YesterdayPopularRecommend.as_view())
]
