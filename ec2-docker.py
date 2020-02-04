#!/usr/bin/env python
import os
import subprocess
from pathlib import Path

from app.config.settings import JSON_FILE

DOCKER_OPTIONS = [
    ('--rm', ''),
    ('-it', ''),
    # '-d' 백그라운드에서 실행하는 옵션
    ('-d', ''),
    ('-p', '80:8000'),
    ('--name', 'instagram'),
    # ('--env', f'AWS_ACCESS_KEY_ID="{aws_access_key}"'),
    # ('--env', f'AWS_SECRET_ACCESS_KEY="{aws_secret_key}"'),
    # ('--env', f'NAVER_CLIENT_ID="{naver_id}"'),
    # ('--env', f'NAVER_CLIENT_SECRET="{naver_secret}"'),
    # ('--env', f'PSQL_USER="{psql_user}"'),
    # ('--env', f'PSQL_PASSWORD="{psql_password}"'),
    # ('--env', f'SECRET_KEY="{secret_key}"'),
]

DOCKER_IMAGE_TAG = 'hyeonggeun2/wps-instagram'
HOME = str(Path.home())
IDENTITY_FILE = os.path.join(HOME, '.ssh', 'study.pem')
SOURCE = os.path.join(HOME, 'projects', 'wps12th', 'instagram')
HOST = '13.125.249.76'
SECRETS_FILE = JSON_FILE


def run(cmd, ignore_error=False):
    process = subprocess.run(cmd, shell=True)
    if not ignore_error:
        process.check_returncode()


def ssh_run(cmd, ignore_error=False):
    # 처음 인증을 넘어갈 수 있음.
    run(f"ssh -i {IDENTITY_FILE} ubuntu@{HOST} -C {cmd}", ignore_error=ignore_error)


# 1.도커 이미지 생성 및 푸쉬
def local_build_push():
    run(f'docker build -t {DOCKER_IMAGE_TAG} .')
    run(f'docker push {DOCKER_IMAGE_TAG}')


# 2.서버 초기설정
def server_init():
    ssh_run('sudo apt update && sudo DEBIAN_FRONTEND=noninteractive apt dist-upgrade -y && sudo apt -y autoremove')
    ssh_run('sudo apt -y install docker.io')


# 3.도커 재실행
def server_pull_run():
    ssh_run('sudo docker stop instagram', ignore_error=True)
    ssh_run(f'sudo docker pull {DOCKER_IMAGE_TAG}')
    ssh_run('sudo docker run {options} {tag} /bin/bash'.format(
        options=' '.join([
            f'{key} {value}' for key, value in DOCKER_OPTIONS
        ]),
        tag=DOCKER_IMAGE_TAG,
    ))


# 4.HOST -> EC2 -> container 로 EC2 전달
def copy_secrets():
    run(f'scp -i {IDENTITY_FILE} {SECRETS_FILE} ubuntu@{HOST}:/tmp', ignore_error=True)
    ssh_run(f'sudo docker cp /tmp/instagram_secrets.json instagram:/srv/instagram')


# 5.container 에서 runserver
def server_runserver():
    ssh_run('sudo docker exec -it -d instagram python /srv/instagram/app/manage.py runserver 0:8000')


# 이 파일이 어디 포함되서 실행되지 않고 단독으로 실행되는 경우만 실행!
if __name__ == '__main__':
    try:
        local_build_push()
        server_init()
        server_pull_run()
        copy_secrets()
        server_runserver()
    except subprocess.CalledProcessError as e:
        print('deploy-docker-secrets Error!')
        print(' cmd:', e.cmd)
        print(' returncode:', e.returncode)
        print(' output:', e.output)
        print(' stdout:', e.stdout)
        print(' stderr:', e.stderr)