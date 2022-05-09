from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,

    HTTP_400_BAD_REQUEST,
)

from post.serializers import PostSerializer
from post.models import Post, Comment

class PostList(APIView):
    serializer_class= PostSerializer

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
    serialzer_class= PostSerializer

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
