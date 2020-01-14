from django import forms

from posts.models import Post


class PostCreateForm(forms.Form):
    images = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={
                'multiple': True
            }
        )
    )
    text = forms.CharField()

    def save(self, request):
        images = request.FILES.getlist('images')
        text = request.POST['text']

        post = Post.objects.create(author=request.user, content=text)

        for image in images:
            post.postimage_set.create(image=image)


class CommentCreateForm(forms.Form):
    comment = forms.CharField(max_length=50)

    def save(self, post, author):
        return post.postcomment_set.create(author=author, content=self.cleaned_data['comment'])
