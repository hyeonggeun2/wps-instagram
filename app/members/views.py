from django.contrib.auth import authenticate, login, get_user_model, logout
from django.shortcuts import render, redirect

# 유저모델을 알아서 찾아서 가져옴(기본 or 커스텀)
from members.forms import SignupForm, LoginForm

User = get_user_model()


def login_view(request):
    if request.user.is_authenticated:
        return redirect('posts:post-list')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('posts:post-list')
        else:
            return redirect('members:login')

    else:
        form = LoginForm()
        context = {
            'form': form
        }

        return render(request, 'members/login.html', context)




def signup_view(request):
    signup_form = SignupForm(data=request.POST)

    email = request.POST['email']
    username = request.POST['username']
    name = request.POST['name']
    password = request.POST['password']

    if signup_form.is_valid():
        new_user = signup_form.save(email=email, username=username, name=name, password=password)
        login(request, new_user)
        return redirect('posts:post-list')


def logout_view(request):
    logout(request)
    return redirect('members:login')
