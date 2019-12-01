FROM python:3.7-alpine

RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code/
RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev libffi-dev openssl-dev
RUN pip install --no-cache-dir -r requirements.txt
ADD . /code/
