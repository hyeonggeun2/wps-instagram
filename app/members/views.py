import json

import requests
from django.contrib.auth import get_user_model, logout, login
from django.http import HttpResponse
from django.shortcuts import render, redirect

# 유저모델을 알아서 찾아서 가져옴(기본 or 커스텀)
from config import settings
from members.forms import SignupForm, LoginForm

User = get_user_model()

# json 파일 불러오기
with open(settings.JSON_FILE) as data_file:
    json_data = json.load(data_file)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('posts:post-list')

    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form.login(request)
            return redirect('posts:post-list')
    else:
        form = LoginForm()

    login_base_url = 'https://nid.naver.com/oauth2.0/authorize'
    login_params = {
        'response_type': 'code',
        'client_id': json_data['NAVER_CLIENT_ID'],
        'redirect_uri': 'http://localhost:8000/members/naver-login/',
        'state': 'RANDOM_STATE',
    }
    login_url = '{base}?{params}'.format(
        base=login_base_url,
        params='&'.join([f'{key}={value}' for key, value in login_params.items()])
    )

    print(login_url)

    context = {
        'form': form,
        'login_url': login_url
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


def naver_login(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
    if not code or not state:
        return HttpResponse('code또는 state가 전달되지 않았습니다.')

    token_base_url = 'https://nid.naver.com/oauth2.0/token'

    token_params = {
        'grant_type': 'authorization_code',
        'client_id': json_data['NAVER_CLIENT_ID'],
        'client_secret': json_data['NAVER_CLIENT_SECRET'],
        'code': code,
        'state': state,
        'redirectURI': 'http://localhost:8000/members/naver-login/',
    }

    token_url = '{base}?{params}'.format(
        base=token_base_url,
        params='&'.join([f'{key}={value}' for key, value in token_params.items()])
    )
    response = requests.get(token_url)

    # 회원 프로필 조회
    access_token = response.json()['access_token']
    print(access_token)

    me_url = "https://openapi.naver.com/v1/nid/me"
    me_headers = {
        'Authorization': f'Bearer {access_token}'
    }

    me_response = requests.get(me_url, headers=me_headers)
    me_response_data = me_response.json()
    print(me_response_data)

    unique_id = me_response_data['response']['id']
    print(unique_id)
    return redirect('posts:post-list')
