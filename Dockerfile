FROM python:3.5

COPY . /opt/web_server_ascii
WORKDIR /opt/web_server_ascii

RUN apt-get update && \
    apt-get install -y nginx python-opencv

RUN pip install -r requirements.txt

