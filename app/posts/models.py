from django.db import models

from members.models import User


class Post(models.Model):
    """
    인스타그램의 포스트
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    # PostLike 를 통한 Many-to-many 구현
    like_users = models.ManyToManyField(User, through='PostLike', symmetrical=False, related_name='like_post_set')
    created = models.DateTimeField(auto_now_add=True)


class PostImage(models.Model):
    """
    각 포스트의 사진
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/images')


class PostComment(models.Model):
    """
    각 포스트의 댓글 (Many-to-one)
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
