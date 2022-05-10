from django.urls import path

from user.views import (
    UserDetail,
    UserList,
    
    RecordList,
)


urlpatterns = [
    path('/users', UserList.as_view()),
    path('/users/<int:pk>', UserDetail.as_view()),
    path('/users/<int:pk>/records', RecordList.as_view()),
]
