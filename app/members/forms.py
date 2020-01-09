from django import forms
from django.http import HttpResponse

from members.models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'please input username'
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'please input password'
            }
        )
    )

class SignupForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField(max_length=30)
    name = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())

    def save(self, email, username, name, password):
        if User.objects.filter(email=email):
            return HttpResponse('<h1>이미 존재하는 이메일 주소입니다.</h1>')
        elif User.objects.filter(username=username):
            return HttpResponse('<h1>이미 존재하는 아이디입니다.</h1>')

        else:
            return User.objects.create(
                email=self.cleaned_data['email'],
                username=self.cleaned_data['username'],
                name=self.cleaned_data['name'],
                password=self.cleaned_data['password']
        )