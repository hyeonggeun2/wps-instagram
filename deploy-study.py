#!/usr/bin/env python
import os
import subprocess
from pathlib import Path

HOME = str(Path.home())
IMAGE_TAG = 'hyeonggeun2/wps-instagram'
IDENTITY_FILE = f"-i {os.path.join(HOME, '.ssh', 'study.pem')}"
EC2_SERVER = 'ubuntu@13.125.249.76'
SECRET_FILE = os.path.join(HOME, 'projects', 'wps12th', 'instagram', 'secrets.json')

DOCKER_OPTIONS = [
    ('--rm', ''),
    ('-it', ''),
    ('-p', '80:80'),
    ('--name', 'instagram'),
    ('-d', ''),
]


def run(command, ignore_error=False):
    if ignore_error:
        subprocess.run(command, shell=True)
    else:
        subprocess.run(command, shell=True).check_returncode()


def ssh_run(command, ignore_error=False):
    run(f'ssh {IDENTITY_FILE} {EC2_SERVER} {command}', ignore_error=ignore_error)


# 1-1. HOST에서 이미지를 build, push
def image_build_push():
    run('poetry export -f requirements.txt > requirements.txt')
    run(f'docker build -t {IMAGE_TAG} .')
    run(f'docker push {IMAGE_TAG}')


# 1-2. EC2에서 우분투 초기설정 및 도커설치
def ec2_setting():
    ssh_run('sudo apt update -y')
    ssh_run('sudo DEBIAN_FRONTEND=noninteractive apt dist-upgrade -y')
    ssh_run('sudo apt autoremove -y')
    ssh_run('sudo apt install docker.io')


# 2. EC2에서 이미지 pull, run(bash)
def ec2_pull_run():
    ssh_run('sudo docker stop instagram', ignore_error=True)
    ssh_run(f'sudo docker pull {IMAGE_TAG}')
    ssh_run('sudo docker run {option} {tag} /bin/bash'.format(
        option=' '.join([
            f'{key} {value}' for key, value in DOCKER_OPTIONS
        ]),
        tag=IMAGE_TAG
    ))


# 3. 시크릿 값 전송
def send_secret_key():
    # 로컬 -> EC2
    run(f'scp {IDENTITY_FILE} {SECRET_FILE} {EC2_SERVER}:/tmp')
    # EC2 -> 컨테이너
    ssh_run('sudo docker cp /tmp/secrets.json instagram:/srv/instagram')


# 4. 컨테이너에서 서버 실행
def runserver_in_container():
    ssh_run('sudo docker exec instagram python manage.py collectstatic')
    ssh_run('sudo docker exec instagram supervisord -c ../.config/supervisord.conf')


if __name__ == '__main__':
    try:
        image_build_push()
        ec2_setting()
        ec2_pull_run()
        send_secret_key()
        runserver_in_container()
    except subprocess.CalledProcessError as Error:
        print('@@@@@@@@@@ ERROR @@@@@@@@@@')
        print(Error.cmd)
