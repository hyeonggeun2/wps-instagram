from time import timezone

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
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        )
    )

    def save(self, author):
        images = self.files.getlist('images')
        text = self.cleaned_data['text']

        post = Post.objects.create(author=author, content=text)

        for image in images:
            post.postimage_set.create(image=image)


class CommentCreateForm(forms.Form):
    comment = forms.CharField(max_length=50)

    def save(self, post, author):
        return post.postcomment_set.create(author=author, content=self.cleaned_data['comment'])

timezone