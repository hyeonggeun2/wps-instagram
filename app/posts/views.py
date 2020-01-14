from django.shortcuts import render, redirect

from .forms import PostCreateForm, CommentCreateForm
from .models import Post, PostLike


def post_list(request):
    comment_form = CommentCreateForm()
    posts = Post.objects.order_by('-pk')
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
        form = PostCreateForm(request.POST)
        form.save(request)
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