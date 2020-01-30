#!/usr/bin/env sh

IDENTIFY_FILE="$HOME/.ssh/nuna.pem"
USER="ubuntu"
IP="54.180.153.158"
HOST="${USER}@${IP}"
SSH_CMD="ssh -i ${IDENTIFY_FILE} ${HOST}"


echo "== Docker 배포 =="

echo "서버 업데이트"
${SSH_CMD} sudo apt update && sudo DEBIAN_FRONTEND=noninteractive apt dist-upgrade -y && apt -y autoremove
echo "python3 pip 설치"
${SSH_CMD} sudo apt -y install python3-pip

echo "EC2에서 docker 설치"
${SSH_CMD} sudo apt-get -y docker.io

echo "screen을 통한 서버 재시작"
echo " - 서버 종료"
${SSH_CMD} screen -X -S runserver quit

echo " - 스크린 실행"
${SSH_CMD} screen -S runserver -d -m

echo " - 스크린에 명령어 추가"
${SSH_CMD} "screen -r runserver -X stuff 'sudo docker run --rm -it -p 80:8000 hyeonggeun2/wps-instagram\n'"

echo "== Docker를 통한 배포완료! =="
