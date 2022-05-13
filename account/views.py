from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,

    HTTP_400_BAD_REQUEST,
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from account.models import Profile
from account.serializers import (
    LikeDislikeSerializer,
    ProfileSerializer,
    UserListSerializer,
    UserDetailSerializer,
    UserRegisterSerializer,
)
from feature.models import Food


User = get_user_model()

class UserList(APIView):
    authentication_classes = (TokenAuthentication,)
    
    def get_authenticators(self):
        if self.request.method == 'POST':
            authentication_classes = ()
        else:
            authentication_classes = (TokenAuthentication, )
        return [auth() for auth in authentication_classes]

    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = (AllowAny,)
        else:
            permission_classes = (IsAuthenticated, IsAdminUser,)
        return [permission() for permission in permission_classes]

    @swagger_auto_schema(   
        operation_id            = '사용자 목록 조회',
        operation_description   = '사용자 목록을 조회합니다.',
        responses               = {200: openapi.Response('', UserListSerializer(many=True))}
    )
    def get(self, request):
        users    = User.objects.filter(is_active=True)
        serializer  = UserListSerializer(users, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    @swagger_auto_schema(   
        operation_id            = '사용자 등록(회원가입)',
        operation_description   = '사용자를 등록합니다.',
        request_body            = UserRegisterSerializer,
        responses               = {201: openapi.Response('', UserRegisterSerializer(many=True))}
    )
    def post(self, request):
        serializer  = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class UserDetail(APIView):
    serializer_class    = UserDetailSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminUser,)

    @swagger_auto_schema(   
        operation_id            = '사용자 조회',
        operation_description   = '사용자를 조회합니다.',
        responses               = {200: openapi.Response('', UserDetailSerializer)}
    )
    def get(self, request, pk):
        user        = User.objects.get(pk=pk)
        serializer  = self.serializer_class(user)
        return Response(serializer.data, status=HTTP_200_OK)

    @swagger_auto_schema(   
        operation_id            = '사용자 정보 수정',
        operation_description   = '사용자 정보를 수정합니다.',
        request_body            = ProfileSerializer,
        responses               = {200: openapi.Response('', ProfileSerializer)}
    )
    def put(self, request, pk):
        profile     = Profile.objects.get(user_id=pk)
        serializer  = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(   
        operation_id            = '사용자 정보 수정',
        operation_description   = '사용자 정보를 수정합니다.',
        request_body            = ProfileSerializer,
        responses               = {200: openapi.Response('', ProfileSerializer)}
    )
    def patch(self, request, pk):
        profile     = Profile.objects.get(user_id=pk)
        serializer  = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(   
        operation_id            = '사용자 삭제(회원탈퇴)',
        operation_description   = '사용자를 비활성화로 변경합니다.',
        responses               = {204: openapi.Response('No Content')}
    )
    def delete(self, request, pk):
        user        = User.objects.get(pk=pk)
        user.is_active = False
        user.save()
        return Response(status=HTTP_204_NO_CONTENT)

class UserProfile(APIView):
    serializer_class    = UserDetailSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(   
        operation_id            = '사용자 조회',
        operation_description   = '사용자를 조회합니다.',
        responses               = {200: openapi.Response('', UserDetailSerializer)}
    )
    def get(self, request):
        user        = request.user
        serializer  = self.serializer_class(user)
        return Response(serializer.data, status=HTTP_200_OK)

    @swagger_auto_schema(   
        operation_id            = '사용자 정보 수정',
        operation_description   = '사용자 정보를 수정합니다.',
        request_body            = ProfileSerializer,
        responses               = {200: openapi.Response('', ProfileSerializer)}
    )
    def put(self, request):
        profile     = request.user.profile
        serializer  = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(   
        operation_id            = '사용자 정보 수정',
        operation_description   = '사용자 정보를 수정합니다.',
        request_body            = ProfileSerializer,
        responses               = {200: openapi.Response('', ProfileSerializer)}
    )
    def patch(self, request):
        profile     = request.user.profile
        serializer  = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(   
        operation_id            = '사용자 삭제(회원탈퇴)',
        operation_description   = '사용자를 비활성화로 변경합니다.',
        responses               = {204: openapi.Response('No Content')}
    )
    def delete(self, request):
        user        = request.user
        user.is_active = False
        user.save()
        return Response(status=HTTP_204_NO_CONTENT)

class LikeList(APIView):
    serializer_class    = LikeDislikeSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes  = (IsAuthenticated,)

    @swagger_auto_schema(   
        operation_id            = '선호 음식 조회',
        operation_description   = '사용자 선호 음식을 조회합니다.',
        responses               = {200: openapi.Response('', serializer_class(many=True))}
    )
    def get(self, request):
        likes       = request.user.profile.likes
        serializer  = self.serializer_class(likes, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

class DislikeList(APIView):
    serializer_class    = LikeDislikeSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes  = (IsAuthenticated,)

    @swagger_auto_schema(   
        operation_id            = '비선호 음식 조회',
        operation_description   = '사용자 비선호 음식을 조회합니다.',
        responses               = {200: openapi.Response('', serializer_class(many=True))}
    )
    def get(self, request):
        dislikes       = request.user.profile.dislikes
        serializer  = self.serializer_class(dislikes, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

class Like(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes  = (IsAuthenticated,)

    @swagger_auto_schema(   
        operation_id            = '선호 음식 추가',
        operation_description   = '사용자 정보에 선호 음식을 추가합니다.',
        responses               = {204: openapi.Response('No Content')}
    )
    def put(self, request, pk):
        likes       = request.user.profile.likes
        dislikes    = request.user.profile.dislikes
        food        = Food.objects.get(pk=pk)
        if dislikes.filter(pk=pk).exists():
            return Response({
                'detail': 'The food is already in dislikes.'
            }, status=HTTP_400_BAD_REQUEST)
        likes.add(food)
        return Response(status=HTTP_204_NO_CONTENT)

    @swagger_auto_schema(   
        operation_id            = '선호 음식 제거',
        operation_description   = '사용자 정보에서 선호 음식을 제거합니다.',
        responses               = {204: openapi.Response('No Content')}
    )
    def delete(self, request, pk):
        likes       = request.user.profile.likes
        food        = Food.objects.get(pk=pk)
        likes.remove(food)
        return Response(status=HTTP_204_NO_CONTENT)


class Dislike(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes  = (IsAuthenticated,)

    @swagger_auto_schema(   
        operation_id            = '비선호 음식 추가',
        operation_description   = '사용자 정보에 선호 음식을 추가합니다.',
        responses               = {204: openapi.Response('No Content')}
    )
    def put(self, request, pk):
        dislikes    = request.user.profile.dislikes
        food        = Food.objects.get(pk=pk)
        dislikes.add(food)
        return Response(status=HTTP_204_NO_CONTENT)

    @swagger_auto_schema(   
        operation_id            = '비선호 음식 제거',
        operation_description   = '사용자 정보에서 선호 음식을 제거합니다.',
        responses               = {204: openapi.Response('No Content')}
    )
    def delete(self, request, pk):
        dislikes    = request.user.profile.dislikes
        food        = Food.objects.get(pk=pk)
        dislikes.remove(food)
        return Response(status=HTTP_204_NO_CONTENT)

class LikeListByUser(APIView):
    serializer_class    = LikeDislikeSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes  = (IsAuthenticated,)

    @swagger_auto_schema(   
        operation_id            = '사용자 선호 음식 조회',
        operation_description   = '특정 사용자의 선호 음식을 조회합니다.',
        responses               = {200: openapi.Response('', serializer_class(many=True))}
    )
    def get(self, request, pk):
        user        = User.objects.get(pk=pk)
        likes       = user.profile.likes
        serializer  = self.serializer_class(likes, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

class DislikeListByUser(APIView):
    serializer_class    = LikeDislikeSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes  = (IsAuthenticated,)

    @swagger_auto_schema(   
        operation_id            = '사용자 비선호 음식 조회',
        operation_description   = '특정 사용자의 비선호 음식을 조회합니다.',
        responses               = {200: openapi.Response('', serializer_class(many=True))}
    )
    def get(self, request, pk):
        user        = User.objects.get(pk=pk)
        dislikes    = user.profile.dislikes
        serializer  = self.serializer_class(dislikes, many=True)
        return Response(serializer.data, status=HTTP_200_OK)



