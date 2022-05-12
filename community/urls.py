from django.urls import path

from community.views import (
    PostList,
    PostDetail,
    
    CategoryList,

    CommentList,
    CommentDelete,
)


urlpatterns = [
    path('/posts', PostList.as_view()),
    path('/posts/<int:pk>', PostDetail.as_view()),

    path('/categories', CategoryList.as_view()),
    
    path('/comments', CommentList.as_view()),
    path('/comments/<int:pk>', CommentDelete.as_view()),
]
