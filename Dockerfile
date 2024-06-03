# Dockerfile for Django project
FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./social_media/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./social_media /app
COPY ./.env /app
COPY ./start.sh /app
RUN chmod +x /app/start.sh