from django.shortcuts import render, redirect

from .forms import PostCreateForm, CommentCreateForm
from .models import Post, PostLike


def post_list(request, tag=None):
    if tag is None:
        posts = Post.objects.order_by('-pk')
    else:
        posts = Post.objects.filter(tags__name__iexact=tag).order_by('-pk')

    comment_form = CommentCreateForm()
    context = {
        'posts': posts,
        'comment_form': comment_form
    }
    return render(request, 'posts/post-list.html', context)


def post_like(request, pk):
    post = Post.objects.get(pk=pk)
    user = request.user
    post_like_qs = post.postlike_set.filter(user=user)

    if post_like_qs:
        post_like_qs.delete()
    else:
        post.postlike_set.create(user=user)

    return redirect('posts:post-list')


def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(request.user)
        # print(form.errors)
        return redirect('posts:post-list')

    else:
        form = PostCreateForm()
    context = {
        'form': form
    }
    return render(request, 'posts/post-create.html', context)


def comment_create(request, post_pk):
    post = Post.objects.get(pk=post_pk)

    form = CommentCreateForm(data=request.POST)
    if form.is_valid():
        form.save(post=post, author=request.user)

    return redirect('posts:post-list')