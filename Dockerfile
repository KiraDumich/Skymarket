FROM python:3

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libffi-dev \
    libyaml-dev

WORKDIR /code

COPY /requirements.txt /

ENV PYTHONUNBUFFERED 1

RUN pip install -r /requirements.txt --no-cache-dir

COPY . .

