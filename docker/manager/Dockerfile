#syntax=docker/dockerfile:1
FROM python:3.10-alpine3.17

RUN apk add --update --no-cache g++ gcc

WORKDIR /src

COPY ./docker/manager/src .

COPY ./docker/manager/requirements.txt .

RUN python3 -m pip install -r requirements.txt

WORKDIR /

COPY docker/manager/start.sh /start.sh

RUN chmod +x /start.sh

RUN ls
