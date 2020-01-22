import os

from django.conf import settings
from django.core.management import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = '현재 포스트, 코멘트, 태그의 갯수를 리턴합니다.'

    def handle(self, *args, **kwargs):
        now = timezone.now()

        with open(os.path.join(settings.MEDIA_ROOT, 'now.txt'), 'at') as f:
            time_str = f'Now: {timezone.localtime(now).strftime("%Y-%m-%d %H:%M:%S")}\n'
            f.write(time_str)
        # post_num = len(Post.objects.all())
        # post_comment_num = len(PostComment.objects.all())
        # tag_num = len(Tag.objects.all())
        # print(f'전체 Posts: {post_num}개\n전체 Comments: {post_comment_num}개\n전체 Tags: {tag_num}개')
