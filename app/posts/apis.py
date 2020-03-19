from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import Post
from posts.serializers import PostSerializer, Serializer, PostImageCreateSerializer, PostCommentSerializer, \
    PostCreateSerializer


# class PostListCreateAPIView(APIView):
#     def get(self, request):
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = Serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(author=self.request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostSerializer
        elif self.request.method == 'POST':
            return PostCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostImageCreateAPIView(APIView):
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        images = request.data.getlist('image')

        for image in images:
            data = {
                'image': image
            }
            serializer = PostImageCreateSerializer(data=data)
            if serializer.is_valid():
                serializer.save(post=post, image=image)

            serializer = PostSerializer(post)
            return Response(serializer.data)


class PostCommentListCreateAPIView(APIView):
    def get(self, request, post_pk):
        post = get_object_or_404(Post, pk=post_pk)
        comments = post.postcomment_set.all()
        serializer = PostCommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, post_pk):
        post = get_object_or_404(Post, pk=post_pk)
        serializer = PostCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, author=request.user)
            return Response(serializer.data)
        return Response(serializer.errors)

# class PostCommentListCreateAPIView(generics.ListCreateAPIView):
#     queryset = PostComment.objects.all()
#     serializer_class = PostCommentSerializer
#
#     def perform_create(self, serializer):
#         post_pk = self.kwargs['post_pk']
#         post = Post.objects.get(pk=post_pk)
#         serializer.save(post=post, author=self.request.user)
#
#     # def get_serializer_class(self):
#     #     if self.request.method == 'GET':
#     #         return PostCommentSerializer
#     #     elif self.request.method == 'POST':
#     #         return PostCommentCreateSerializer
