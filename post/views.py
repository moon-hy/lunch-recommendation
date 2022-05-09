from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,

    HTTP_400_BAD_REQUEST,
)

from post.serializers import CommentSerializer, PostListSerializer, PostDetailSerializer
from post.models import Post, Comment

class PostList(APIView):
    serializer_class= PostListSerializer
    permission_classes  = (IsAuthenticated, )

    # def get_permissions(self):
    #     permission_classes = ()

    #     if self.request.method == 'POST':
    #         permission_classes = (IsAuthenticated, )

    #     return [permission() for permission in permission_classes]

    def get(self, request):
        posts       = Post.objects.all()
        serializer  = self.serializer_class(posts, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request):
        serializer  = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class PostDetail(APIView):
    serialzer_class     = PostDetailSerializer
    permission_classes  = (IsAuthenticated, )

    def get(self, request, pk):
        post        = Post.objects.get(pk=pk)
        serializer  = self.serialzer_class(post)
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, pk):
        post        = Post.objects.get(pk=pk)
        serializer  = self.serialzer_class(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        post        = Post.objects.get(pk=pk)
        serializer  = self.serialzer_class(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post        = Post.objects.get(pk=pk)
        post.delete()
        return Response(status=HTTP_204_NO_CONTENT)

class PostCommentList(APIView):
    serializer_class    = CommentSerializer
    permission_classes  = (IsAuthenticated, )

    def get(self, request, pk):
        comments    = Comment.objects.filter(post=pk)
        serializer  = self.serializer_class(comments, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request, pk):
        serializer  = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post_id=pk)
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
class CommentDetail(APIView):
    serializer_class    = CommentSerializer
    permission_classes  = (IsAuthenticated, )

    def get(self, request, pk):
        comment     = Comment.objects.get(pk=pk)
        serializer  = self.serializer_class(comment)
        return Response(serializer.data, status=HTTP_200_OK)


    def delete(self, request, pk):
        comment     = Comment.objects.get(pk=pk)
        comment.delete()
        return Response(status=HTTP_204_NO_CONTENT)
