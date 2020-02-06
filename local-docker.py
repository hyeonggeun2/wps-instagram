#!/usr/bin/env python
import subprocess

from app.config import settings

# settings.py 에서 얻어온 SECRET를 가져옴
SECRET = settings.SECRET

# 넘겨주어야 할 SECRET 값들을 변수로 만들어 줌
aws_access_key = SECRET['AWS_ACCESS_KEY_ID']
aws_secret_key = SECRET['AWS_SECRET_ACCESS_KEY']
secret_key = SECRET['SECRET_KEY']
naver_id = SECRET['NAVER_CLIENT_ID']
naver_secret = SECRET['NAVER_CLIENT_SECRET']
psql_user = SECRET['PSQL_USER']
psql_password = SECRET['PSQL_PASSWORD']

DOCKER_OPTIONS = [
    ('--rm', ''),
    ('-it', ''),
    ('-p', '8001:80'),
    ('--name', 'instagram'),
    ('--env', f'AWS_ACCESS_KEY_ID="{aws_access_key}"'),
    ('--env', f'AWS_SECRET_ACCESS_KEY="{aws_secret_key}"'),
    ('--env', f'NAVER_CLIENT_ID="{naver_id}"'),
    ('--env', f'NAVER_CLIENT_SECRET="{naver_secret}"'),
    ('--env', f'PSQL_USER="{psql_user}"'),
    ('--env', f'PSQL_PASSWORD="{psql_password}"'),
    ('--env', f'SECRET_KEY="{secret_key}"'),
]

subprocess.run('docker build -t hyeonggeun2/wps-instagram -f Dockerfile .', shell=True)
subprocess.run('docker stop instagram', shell=True)
subprocess.run('docker run {options} hyeonggeun2/wps-instagram /bin/bash'.format(
    options=' '.join(
        [f'{key} {value}' for key, value in DOCKER_OPTIONS]
    )
), shell=True)
