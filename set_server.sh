#!/usr/bin/env sh
IDENTIFY_FILE="$HOME/.ssh/wps12th.pem"
HOST="ubuntu@52.78.47.78"
ORIGIN_SOURCE="$HOME/projects/wps12th/instagram"
DEST_SOURCE="/home/ubuntu/projects/instgram"
SSH_CMD="ssh -i ${IDENTIFY_FILE} ${HOST}"

echo "서버 OS 업데이트"
${SSH_CMD} sudo apt update -y
${SSH_CMD} sudo apt dist-upgrade -y

echo "python3 pip 설치"
${SSH_CMD} sudo apt install -q python3-pip

