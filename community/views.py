from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,

    HTTP_400_BAD_REQUEST,
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from community.serializers import (
    CategorySerializer,
    CommentCreateSerializer,
    PostListSerializer,
    PostDetailSerializer
)
from community.models import Category, Post, Comment
from core.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly

class PostList(APIView):
    serializer_class= PostListSerializer
    permission_classes  = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(   
        operation_id            = '게시글 목록 조회',
        operation_description   = '게시글 목록을 조회합니다.',
        responses               = {200: openapi.Response('', PostListSerializer(many=True))}
    )
    def get(self, request):
        posts       = Post.objects.all()

        if c := request.query_params.get('c'):
            posts   = posts.filter(category=c)

        if q := request.query_params.get('q'):
            posts   = posts.filter(title__icontains=q)

        if u := request.query_params.get('u'):
            posts   = posts.filter(user__username__icontains=u)

        if s := request.query_params.get('s'):
            if s == 'comment':
                posts = posts.annotate(
                    count=Count('comments')
                    ).order_by('-count')

        serializer  = self.serializer_class(posts, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    @swagger_auto_schema(   
        operation_id            = '게시글 등록',
        operation_description   = '게시글을 등록합니다.',
        request_body            = PostListSerializer,
        responses               = {201: openapi.Response('', PostListSerializer)}
    )
    def post(self, request):
        serializer  = PostListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class PostDetail(APIView):
    serialzer_class     = PostDetailSerializer
    permission_classes  = (IsAuthenticated, IsOwnerOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    def get_object(self, request, pk):
        post        = Post.objects.get(pk=pk)
        self.check_object_permissions(request, post)
        return post

    @swagger_auto_schema(   
        operation_id            = '게시글 조회',
        operation_description   = '게시글을 조회합니다.',
        responses               = {200: openapi.Response('', PostDetailSerializer)}
    )
    def get(self, request, pk):
        post        = self.get_object(request, pk)
        serializer  = self.serialzer_class(post)
        return Response(serializer.data, status=HTTP_200_OK)

    @swagger_auto_schema(   
        operation_id            = '댓글 등록',
        operation_description   = '게시글에 댓글을 등록합니다.',
        request_body            = CommentCreateSerializer,
        responses               = {201: openapi.Response('', CommentCreateSerializer)}
    )
    def post(self, request, pk):
        serializer  = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post_id=pk)
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(   
        operation_id            = '게시글 수정',
        operation_description   = '게시글을 수정합니다.',
        request_body            = PostDetailSerializer,
        responses               = {200: openapi.Response('', PostDetailSerializer)}
    )
    def put(self, request, pk):
        post        = self.get_object(request, pk)
        serializer  = self.serialzer_class(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(   
        operation_id            = '게시글 수정',
        operation_description   = '게시글을 수정합니다.',
        request_body            = PostDetailSerializer,
        responses               = {200: openapi.Response('', PostDetailSerializer)}
    )
    def patch(self, request, pk):
        post        = self.get_object(request, pk)
        serializer  = self.serialzer_class(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(   
        operation_id            = '게시글 삭제',
        operation_description   = '게시글을 삭제합니다.',
        responses               = {204: openapi.Response('No Content')}
    )
    def delete(self, request, pk):
        post        = self.get_object(request, pk)
        post.delete()
        return Response(status=HTTP_204_NO_CONTENT)

class CategoryList(APIView):
    serializer_class    = CategorySerializer
    permission_classes  = (IsAuthenticated, IsAdminOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(   
        operation_id            = '카테고리 목록 조회',
        operation_description   = '카테고리 목록을 조회합니다.',
        responses               = {200: openapi.Response('', CategorySerializer(many=True))}
    )
    def get(self, request):
        categories      = Category.objects.all()
        serializer      = self.serializer_class(categories, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    @swagger_auto_schema(   
        operation_id            = '카테고리 추가',
        operation_description   = '게시글 카테고리 목록을 추가합니다.',
        request_body            = CategorySerializer,
        responses               = {200: openapi.Response('', CategorySerializer)}
    )
    def post(self, request):
        serializer      = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class CategoryDetail(APIView):
    pass

class CommentDelete(APIView):
    permission_classes  = (IsAuthenticated, IsOwnerOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    
    def get_object(self, pk):
        comment         = Comment.objects.get(pk=pk)
        self.check_object_permissions(self.request, comment)
        return comment

    @swagger_auto_schema(   
        operation_id            = '댓글 삭제',
        operation_description   = '댓글을 삭제합니다.',
        responses               = {204: openapi.Response('No Content')}
    )
    def delete(self, request, pk):
        comment         = self.get_object(pk)
        comment.delete()
        return Response(status=HTTP_204_NO_CONTENT)
