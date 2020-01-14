import re

from django.db import models

from members.models import User


class Post(models.Model):
    TAG_PATTERN = re.compile(r'#(\w+)')
    """
    인스타그램의 포스트
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    # PostLike 를 통한 Many-to-many 구현
    like_users = models.ManyToManyField(User, through='PostLike', symmetrical=False, related_name='like_post_set')
    created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', verbose_name='해시태그 목록', related_name='posts', blank=True)

    def __str__(self):
        return f'글쓴이: {self.author}, 내용: {self.content}, 좋아요: {self.like_users}, 작성일: {self.created}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        tags = list(set(re.findall(self.TAG_PATTERN, self.content)))
        real_tag = [Tag.objects.get_or_create(name=tag)[0] for tag in tags]

        self.tags.set(real_tag)


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


class Tag(models.Model):
    name = models.CharField('태그명', max_length=100)

    def __str__(self):
        return self.name
