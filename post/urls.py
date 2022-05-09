from django.urls import path, include

from post.views import (
    PostList,
    PostDetail,
)


urlpatterns = [
    path('', PostList.as_view()),
    path('/<int:pk>', PostDetail.as_view()),
]
