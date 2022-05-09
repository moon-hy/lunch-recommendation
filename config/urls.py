from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', )
    path('api/post', include('post.urls')),
    path('api/food', include('food.urls')),
    path('api/auth', include('authentication.urls')),
    path('api/user', include('user.urls')),
]
