from tokenize import Token
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,

    HTTP_400_BAD_REQUEST,
)

from user.models import Profile
from user.serializers import (
    ProfileSerializer,
    UserListSerializer,
    UserDetailSerializer,
    UserRegisterSerializer,
)


User = get_user_model()

class UserList(APIView):
    permission_classes  = [AllowAny]

    def get(self, request):
        users    = User.objects.all()
        serializer  = UserListSerializer(users, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request):
        serializer  = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class UserDetail(APIView):
    serializer_class    = UserDetailSerializer
    authentication_classes = [TokenAuthentication]
    # permission_classes = []

    def get(self, request, pk):
        user        = User.objects.get(pk=pk)
        serializer  = self.serializer_class(user)
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, pk):
        profile     = Profile.objects.get(user_id=pk)
        serializer  = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        profile     = Profile.objects.get(user_id=pk)
        serializer  = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        user        = User.objects.get(pk=pk)
        user.is_activate = False
        user.save()
        return Response(status=HTTP_204_NO_CONTENT)

