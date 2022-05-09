from django.urls import path, include

from post.views import (
    PostList,
    PostDetail,
    PostCommentList,
    
    CommentDetail
)


urlpatterns = [
    path('', PostList.as_view()),
    path('/<int:pk>', PostDetail.as_view()),
    path('/<int:pk>/comments', PostCommentList.as_view()),
    path('/comments/<int:pk>', CommentDetail.as_view()),
]
