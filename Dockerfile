FROM debian:12.5
MAINTAINER Tran Dinh Hoan
WORKDIR /app
EXPOSE 80
COPY . /app/
RUN apt update && apt install netselect-apt -y
RUN netselect-apt -c vietnam -t 15 -a amd64 -n jessie && \
    apt install -y pkg-config python3-dev default-libmysqlclient-dev build-essential python3-pip python3 && \
    rm /usr/lib/python3.11/EXTERNALLY-MANAGED && \
    pip3 install -r requirements.txt --default-timeout=100 future

ENTRYPOINT python3 manage.py runserver 0.0.0.0:80