FROM python:3.9.18-alpine
RUN mkdir /app
ENV TZ="Asia/Ho_Chi_Minh"
ADD . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
CMD ["python", "app.py"]