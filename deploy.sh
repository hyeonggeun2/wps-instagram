#!/usr/bin/env sh
IDENTITY_FILE="$HOME/.ssh/study.pem"
HOST="ubuntu@13.125.249.76"
ORIGIN_SOURCE="$HOME/projects/wps12th/instagram/"
DEST_SOURCE="/home/ubuntu/projects"
SSH_CMD="ssh -i ${IDENTITY_FILE} ${HOST}"
echo "== runserver 배포 =="
# 숙제
# 다시 실행되는 서버 만들기
# > HOST만 바꾸고 이 스크립트를 실행하면 전체 서버가 세팅되고 runserver된 화면 볼 수 있도록 하기
# pip freeze
# 서버 초기설정

echo "apt update & upgrade & autoremove"
${SSH_CMD} -C 'sudo apt update && sudo DEBIAN_FRONTEND=noninteractive apt dist-upgrade -y && apt -y autoremove'
echo "apt install python3-pip"
${SSH_CMD} -C 'sudo apt -y install python3-pip'

echo "pip freeze"
"$HOME"/.pyenv/versions/3.7.5/envs/wps-instagram-env/bin/pip freeze > "$HOME"/projects/wps12th/instagram/requirements.txt
# 기존 폴더 삭제
echo "1. 기존 폴더 삭제"
${SSH_CMD} sudo rm -rf ${DEST_SOURCE}
#ssh -i ~/.ssh/wps12th.pem ubuntu@13.125.213.68 rm -rf /home/ubuntu/projects/instagram
# 로컬에 있는 파일 업로드
echo "2. 로컬 파일 업로드"
${SSH_CMD} mkdir -p ${DEST_SOURCE}
scp -i "${IDENTITY_FILE}" -r "${ORIGIN_SOURCE}" ${HOST}:${DEST_SOURCE}
#scp -i ~/.ssh/wps12th.pem -r ~/projects/wps12th/instagram ubuntu@13.125.213.68:/home/ubuntu/projects/
# pip install
echo "pip install"
${SSH_CMD} pip3 install -q -r /home/ubuntu/projects/instagram/requirements.txt
echo "3. Screen 실행"
# 실행중이던 screen 세션 종료
${SSH_CMD} -C 'screen -X -S runserver quit'
#ssh -i ~/.ssh/wps12th.pem ubuntu@13.125.213.68 -C 'screen -X -S runserver quit'
# screen 실행
${SSH_CMD} -C 'screen -S runserver -d -m'
#ssh -i ~/.ssh/wps12th.pem ubuntu@13.125.213.68 -C 'screen -S runserver -d -m'
# 실행중인 세션에 명령어 전달
${SSH_CMD} -C "screen -r runserver -X stuff 'sudo python3 /home/ubuntu/projects/instagram/app/manage.py runserver 0:80\n'"
#ssh -i ~/.ssh/wps12th.pem ubuntu@13.125.213.68 -C "screen -r runserver -X stuff $'sudo python3 /home/ubuntu/projects/instagram/app/manage.py runserver 0:80\n'"
echo "== 배포 완료 =="

