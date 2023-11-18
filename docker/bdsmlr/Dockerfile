#syntax=docker/dockerfile:1
FROM python:3.10

WORKDIR /src

COPY ./docker/bdsmlr/src .

COPY ./docker/bdsmlr/requirements.txt .

COPY ./docker/bdsmlr/run_tests.sh .

RUN python3 -m pip install -r requirements.txt

RUN chmod +x run_tests.sh
