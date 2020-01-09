from django import forms


class PostCreateForm(forms.Form):
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    text = forms.CharField()


class CommentCreateForm(forms.Form):
    comment = forms.CharField(max_length=50)

    def save(self, post, author):
        return post.postcomment_set.create(author=author, content=self.cleaned_data['comment'])