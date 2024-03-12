FROM python:3.13.0a4-slim-bullseye
MAINTAINER Tran Dinh Hoan
WORKDIR /app
EXPOSE 80
COPY ./tot_nghiep/* /app/
RUN apt update && \
    apt install -y pkg-config python3-dev default-libmysqlclient-dev build-essential && \
    pip install -r requirements.txt --default-timeout=100 future

ENTRYPOINT python3 manage.py runserver 0.0.0.0:80