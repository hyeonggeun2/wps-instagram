"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 2.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import json
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_ROOT = os.path.dirname(BASE_DIR)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PROJECT_ROOT, '.media')

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(PROJECT_ROOT, '.static')

# load secret.json in drop_box
# HOME_DIR = expanduser("~")
HOME_DIR = str(Path.home())
DROP_BOX = os.path.join(HOME_DIR, 'Dropbox')
SECRETS_DIR = os.path.join(DROP_BOX, '.secret_key')
JSON_FILE = os.path.join(SECRETS_DIR, 'instagram_secrets.json')
EC2_SECRETS = os.path.join(PROJECT_ROOT, 'secrets.json')

# json 파일 불러오기
try:
    SECRET = json.load(open(JSON_FILE))
except FileNotFoundError:
    try:
        SECRET = json.load(open(EC2_SECRETS))
    except FileNotFoundError:
        SECRET = {
            'AWS_ACCESS_KEY_ID': os.environ.get('AWS_ACCESS_KEY_ID'),
            'AWS_SECRET_ACCESS_KEY': os.environ.get('AWS_SECRET_ACCESS_KEY'),
            'SECRET_KEY': os.environ.get('SECRET_KEY'),
            'NAVER_CLIENT_ID': os.environ.get('NAVER_CLIENT_ID'),
            'NAVER_CLIENT_SECRET': os.environ.get('NAVER_CLIENT_SECRET'),
            'PSQL_USER': os.environ.get('PSQL_USER'),
            'PSQL_PASSWORD': os.environ.get('PSQL_PASSWORD'),
        }

# with open(JSON_FILE) as data_file:
#     json_data = json.load(data_file)

# django-storages
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# IAM 에서 가져온 키와 아이디를 적음
# S3Full~을 설정해줬으니까 접근할 수 있는 것.
AWS_ACCESS_KEY_ID = SECRET['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = SECRET['AWS_SECRET_ACCESS_KEY']

AWS_STORAGE_BUCKET_NAME = 'wps-instagram-db3'
AWS_AUTO_CREATE_BUCKET = True
AWS_DEFAULT_ACL = 'private'
AWS_S3_REGION_NAME = 'ap-northeast-2'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECRET['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '*',
    # 기본적인 주소 외에 접근을 허용할 주소를 설정할 수 있음
]
# 유저 모델? 추가
AUTH_USER_MODEL = 'members.User'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'members.apps.MembersConfig',
    'posts.apps.PostsConfig',
    'django_extensions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'instagram',
        'USER': SECRET['PSQL_USER'],
        'PASSWORD': SECRET['PSQL_PASSWORD'],
        'HOST': 'hyegg.c2xnwrnlzxkz.ap-northeast-2.rds.amazonaws.com',
        'PORT': 5432,
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
