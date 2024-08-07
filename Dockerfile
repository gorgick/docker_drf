FROM python:3.8-alpine3.16

COPY requirements.txt /temp/requirements.txt
COPY blogs /blogs
WORKDIR /blogs
EXPOSE 8000

RUN apk add postgresql-client build-base postgresql-dev

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password blogs-user
USER blogs-user