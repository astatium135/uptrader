FROM python:3.9-alpine

WORKDIR /web

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./run.sh .
RUN chmod +x ./run.sh

ENTRYPOINT [ "/bin/sh", "./run.sh" ]
