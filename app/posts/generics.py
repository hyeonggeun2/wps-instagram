from rest_framework import generics

from posts.models import Post, PostImage
from posts.serializers import PostSerializer, PostCreateSerializer, PostImageCreateSerializer


class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostSerializer
        elif self.request.method == 'POST':
            return PostCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostImageCreateAPIView(generics.CreateAPIView):
    queryset = PostImage.objects.all()
    serializer_class = PostImageCreateSerializer
