from django.urls import path

from recommendation.views import (
    InterestPopularRecommend,
    InterestUserRecommend,
    RandomRecommend,
    YesterdayPopularRecommend
)


urlpatterns = [
    path('random', RandomRecommend.as_view()),
    path('yesterday-popular', YesterdayPopularRecommend.as_view()),
    path('interest-popular', InterestPopularRecommend.as_view()),
    path('interest-user', InterestUserRecommend.as_view()),
]
