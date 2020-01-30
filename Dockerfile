FROM        python:3.7-slim

RUN         apt -y update && apt -y dist-upgrade

# requirement만 먼저 복사해서 실행시킴 (캐시를 사용하기 위해)
#  -? COPY시 requirement가 안바뀌어도 소스코드가 하나라도 바뀌면 다시 설치하기 때문에
COPY        ./requirements.txt /tmp/
RUN         pip install -r /tmp/requirements.txt

COPY        . /srv/instagram
WORKDIR     srv/instagram/app

CMD         python manage.py runserver 0:8000