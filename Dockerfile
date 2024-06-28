FROM python:3

WORKDIR /code

COPY /requirements.txt /
# Устанавливает переменную окружения, которая гарантирует, что вывод из python будет отправлен прямо в терминал без предварительной буферизации
ENV PYTHONUNBUFFERED 1

RUN pip install -r /requirements.txt --no-cache-dir

COPY . .

