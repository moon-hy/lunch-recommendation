from django.urls import path, include

from post.views import (
    PostList,
    PostDetail,
    PostCommentList,
    
    CommentDetail
)


urlpatterns = [
    path('/posts', PostList.as_view()),
    path('/posts/<int:pk>', PostDetail.as_view()),
    path('/posts/<int:pk>/comments', PostCommentList.as_view()),
    path('/comments/<int:pk>', CommentDetail.as_view()),
]
