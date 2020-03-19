from rest_framework import serializers

from members.serializers import UserSerializer
from posts.models import Post, PostImage, PostComment


class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = (
            'pk',
            'content',
        )


class PostCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = (
            'content',
        )

    def to_representation(self, instance):
        return PostCommentSerializer(instance).data


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    postcomment_set = PostCommentSerializer(many=True)

    class Meta:
        model = Post
        fields = (
            'pk',
            'author',
            'content',
            'postcomment_set',
            'postimage_set',
        )


class PostCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField()
    )

    class Meta:
        model = Post
        fields = (
            'content',
            'images',
        )

    def create(self, validated_data):
        images = validated_data.pop('images')
        # 포스트 객체가 하나 생김.
        post = super().create(validated_data)
        for image in images:
            serializer = PostImageCreateSerializer(data={'image': image})
            if serializer.is_valid():
                serializer.save(post=post)
        return post

    def to_representation(self, instance):
        return PostSerializer(instance).data


class PostImageCreateSerializer(serializers.ModelSerializer):
    # image = Base64ImageField()
    class Meta:
        model = PostImage
        fields = (
            'image',
        )

    # def create(self, validated_data):
    #     image = validated_data.pop('image')
    #
    #     return PostImage.objects.create(image=image)
