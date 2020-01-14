from django.contrib import admin

from posts.models import Post, PostImage, PostComment, PostLike, Tag


class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1


class PostCommentInline(admin.TabularInline):
    model = PostComment
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'created')
    # 접속할 때 다른곳에도 링크를 걸어줄 수 있음.
    # list_display_links = ('author', 'content')
    inlines = [
        PostImageInline,
        PostCommentInline,
    ]
    # 튜플이기 때문에 무조건 ,이 와야 함
    readonly_fields = ('tags',)


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    pass


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    pass


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
