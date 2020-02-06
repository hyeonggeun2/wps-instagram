#!/usr/bin/env python
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("cmd", type=str, nargs=argparse.REMAINDER)
args = parser.parse_args()

DOCKER_OPTIONS = [
    ('--rm', ''),
    ('-it', ''),
    # background로 실행하는 옵션 추가
    ('-d', ''),
    ('-p', '8001:80'),
    ('--name', 'instagram'),
]
DOCKER_IMAGE_TAG = 'hyeonggeun2/wps-instagram'

subprocess.run('poetry export -f requirements.txt > requirements.txt', shell=True)
subprocess.run(f'docker build -t {DOCKER_IMAGE_TAG} .', shell=True)
subprocess.run(f'docker stop instagram', shell=True)

# secrets.json이 없는 상태로 docker run으로 bash를 실행 -> background로 들어감
subprocess.run('docker run {options} {tag} /bin/bash'.format(
    options=' '.join([
        f'{key} {value}' for key, value in DOCKER_OPTIONS
    ]),
    tag=DOCKER_IMAGE_TAG,
), shell=True)

# secrets.json을 전송
subprocess.run('docker cp secrets.json instagram:/srv/instagram', shell=True)

subprocess.run('docker exec instagram python manage.py collectstatic --noinput', shell=True)

# bash실행
subprocess.run('docker exec -it instagram {cmd}'.format(
    cmd=' '.join(args.cmd) if args.cmd else 'supervisord -c ../.config/supervisord.conf -n',
), shell=True)

# runserver명령을 전송
# subprocess.run('docker exec -it instagram python manage.py runserver 0:8000', shell=True)
