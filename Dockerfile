FROM python:3.5

COPY . /opt/web_server_ascii
WORKDIR /opt/web_server_ascii

RUN apt-get update && \
    apt-get install -y nginx python-opencv

RUN pip install -r requirements.txt

RUN mv static /www/data/

RUN cp web_server_nginx.conf /etc/nginx/sites-available/ &&
    ln -s /etc/nginx/sites-available/web_server_nginx.conf /etc/nginx/sites-enabled/

