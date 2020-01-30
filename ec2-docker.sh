#!/usr/bin/env sh

IDENTIFY_FILE="$HOME/.ssh/nuna.pem"
USER="ubuntu"
IP="13.124.45.97"
HOST="${USER}@${IP}"
ORIGIN_SOURCE="$HOME/projects/wps12th/instagram/"
DOCKER_REPO="hyeonggeun2/wps-instagram"
SSH_CMD="ssh -i ${IDENTIFY_FILE} ${HOST}"



echo "== Docker 배포 =="

echo "서버 업데이트"
${SSH_CMD} sudo apt update && sudo DEBIAN_FRONTEND=noninteractive apt dist-upgrade -y && sudo apt -y autoremove

echo "EC2에서 docker 설치"
${SSH_CMD} sudo apt install -y docker.io

echo "docker build"
poetry export -f requirements.txt > requirements.txt
docker build -q -t ${DOCKER_REPO} -f Dockerfile "${ORIGIN_SOURCE}"

echo "docker push"
docker push ${DOCKER_REPO}

echo "docker stop"
${SSH_CMD} sudo docker stop instagram

echo "docker pull"
${SSH_CMD} sudo docker pull ${DOCKER_REPO}

echo "screen을 통한 서버 재시작"
echo " - 서버 종료"
${SSH_CMD} screen -X -S runserver quit

echo " - 스크린 실행"
${SSH_CMD} screen -S runserver -d -m

echo " - 스크린에 명령어 추가"
${SSH_CMD} "screen -r runserver -X stuff 'sudo docker run --rm -it -p 80:8000 --name=instagram hyeonggeun2/wps-instagram\n'"

echo "== Docker를 통한 배포완료! =="
