from django.contrib.auth import authenticate, login, get_user_model, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

# 유저모델을 알아서 찾아서 가져옴(기본 or 커스텀)
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
        return render(request, 'members/login.html')


def signup_view(request):
    """
    Template: index.html을 그대로 사용
        action만 이쪽으로
    URL: /members/signup/
    User에 name필드를 추가
        email
        username
        name
        password
    를 전달받아, 새로운 User를 생성한다
    생성시, User.objects.create_user() 메서드를 사용한다
    이미 존재하는 username또는 email을 입력한 경우,
    "이미 사용중인 username/email입니다" 라는 메시지를 HttpResponse로 돌려준다

    생성에 성공하면 로그인 처리 후 (위의 login_view를 참조) posts:post-list로 redirect처리
    :param request:
    :return:
    """
    email = request.POST['email']
    username = request.POST['username']
    name = request.POST['name']
    password = request.POST['password']
    users = User.objects

    if users.filter(email=email):
        return HttpResponse('<h1>이미 존재하는 이메일 주소입니다.</h1>')

    elif users.filter(username=username):
        return HttpResponse('<h1>이미 존재하는 아이디입니다.</h1>')

    else:
        new_user = User.objects.create_user(email=email, username=username, name=name, password=password)
        login(request, new_user)
        return redirect('posts:post-list')


def logout_view(request):
    logout(request)
    return redirect('members:login')
