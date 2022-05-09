from django.urls import path

from user.views import (
    UserDetail,
    UserList
)


urlpatterns = [
    path('', UserList.as_view()),
    path('/<int:pk>', UserDetail.as_view())
]
