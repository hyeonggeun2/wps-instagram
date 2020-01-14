from django import forms
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError

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

    def clean(self):
        # Form.clean 에서는 cleaned_data 에 접근 가능
        # 여기에는 이 From 이 가진 모든 field 에서 리턴된 데이터가 key: value 형태로 들어있음
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if not user:
            raise ValidationError('Username 또는 Password 가 맞지 않습니다.')
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        login(request, user)


class SignupForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'please input email'
            }
        )
    )

    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'please input username'
            }
        )
    )

    name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'please input name'
            }
        )
    )

    password = forms.CharField(
        max_length=30,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'please input password'
            }
        )
    )

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email):
            raise ValidationError('이미 사용중인 email입니다.')

        return email

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username=username):
            raise ValidationError('이미 사용중인 username입니다.')

        return username

    def signup(self):
        email = self.cleaned_data['email']
        username = self.cleaned_data['username']
        name = self.cleaned_data['name']
        password = self.cleaned_data['password']

        return User.objects.create_user(email=email, username=username, name=name, password=password)
