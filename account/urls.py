from django.urls import path

from account.views import (
    DislikeListByUser,
    LikeListByUser,
    UserDetail,
    Like,
    Dislike,
    LikeList,
    DislikeList,
    UserList,
    UserProfile,
    Interest,
)


urlpatterns = [
    path('users', UserList.as_view()),
    path('users/<int:pk>', UserDetail.as_view()),

    path('user', UserProfile.as_view()),
    
    path('user/interest', Interest.as_view()),

    path('user/likes', LikeList.as_view()),
    path('user/likes/<int:pk>', Like.as_view()),

    path('user/dislikes', DislikeList.as_view()),
    path('user/dislikes/<int:pk>', Dislike.as_view()),

    path('users/<int:pk>/likes', LikeListByUser.as_view()),
    path('users/<int:pk>/dislikes', DislikeListByUser.as_view()),
]
