from django import forms


class PostCreateForm(forms.Form):
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    text = forms.CharField()
