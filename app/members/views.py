from django.contrib.auth import get_user_model, logout, login
from django.shortcuts import render, redirect

# 유저모델을 알아서 찾아서 가져옴(기본 or 커스텀)
from members.forms import SignupForm, LoginForm

User = get_user_model()


def login_view(request):
    form = LoginForm()

    if request.user.is_authenticated:
        return redirect('posts:post-list')

    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form.login(request)
            return redirect('posts:post-list')
    else:
        form = LoginForm()

    context = {
        'form': form
    }

    return render(request, 'members/login.html', context)


def signup_view(request):
    if request.method == 'POST':
        signup_form = SignupForm(data=request.POST)

        if signup_form.is_valid():
            user = signup_form.signup()
            login(request, user)
            return redirect('posts:post-list')

    else:
        signup_form = SignupForm()

    context = {
        'signup_form': signup_form
    }

    return render(request, 'members/signup.html', context)


def logout_view(request):
    logout(request)
    return redirect('members:login')
