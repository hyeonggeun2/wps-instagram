#!/usr/bin/env sh
IDENTIFY_FILE="$HOME/.ssh/wps12th.pem"
IP="52.78.47.78"
HOST="ubuntu@${IP}"
ORIGIN_SOURCE="$HOME/projects/wps12th/instagram"
DEST_SOURCE="/home/ubuntu/projects/instagram"
SSH_CMD="ssh -i ${IDENTIFY_FILE} ${HOST}"



echo "== runserver 배포 =="

echo "0. pip freeze"
"$HOME"/.pyenv/versions/3.7.5/envs/wps-instagram-env/bin/pip freeze > "$HOME"/projects/wps12th/instagram/requirements.txt

echo "1. 기존 폴더 삭제"
${SSH_CMD} sudo rm -rf ${DEST_SOURCE}

echo "2. 로컬에 있는 파일 업로드"
${SSH_CMD} mkdir projects
scp -q -i "${IDENTIFY_FILE}" -r "${ORIGIN_SOURCE}" ${HOST}:${DEST_SOURCE}

echo "3. pip install"
${SSH_CMD} sudo pip3 install -q -r /home/ubuntu/projects/instagram/requirements.txt

echo "4. screen을 통한 서버 재시작"
echo " - 서버 종료"
${SSH_CMD} screen -X -S runserver quit

echo " - 스크린 실행"
${SSH_CMD} screen -S runserver -d -m

echo " - 스크린에 명령어 추가"
${SSH_CMD} "screen -r runserver -X stuff 'sudo python3 /home/ubuntu/projects/instagram/app/manage.py runserver 0:80\n'"
echo "== 배포완료! =="

echo "http://${IP}"
