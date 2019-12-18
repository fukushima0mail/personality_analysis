FROM python:3.7-alpine

RUN mkdir /code
WORKDIR /code

ADD ./docker-requirements.txt /code/
RUN apk update \
    && apk add mysql-client \
    && apk add make automake gcc g++ subversion python3-dev libffi-dev openssl-dev
RUN pip install --no-cache-dir -r docker-requirements.txt
RUN pip install pandas --no-build-isolation
COPY ./entrypoint.sh /
COPY ./testdata /
CMD ["/entrypoint.sh"]
