from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from .models import Post
from .serializers import PostSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer

    def list(self, request):
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, id=pk)
        if post.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, id=pk)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid() and post.author == request.user:
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, pk):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, id=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs.get('id'))
        queryset = post.comments.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def list(self, request, id):
        post = get_object_or_404(Post, id=id)
        queryset = post.comments.all()
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def partial_update(self, request, id, pk):
        comment = get_object_or_404(self.get_queryset(), id=pk)
        serializer = CommentSerializer(comment,
                                       data=request.data, partial=True)
        if serializer.is_valid() and comment.author == request.user:
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, id, pk):
        comment = get_object_or_404(self.get_queryset(), id=pk)
        if comment.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
