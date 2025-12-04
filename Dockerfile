FROM python:3.13-slim

RUN apt-get update && apt-get install -y tzdata \
    && ln -fs /usr/share/zoneinfo/Europe/Moscow /etc/localtime \
    && dpkg-reconfigure -f noninteractive tzdata


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=./src
WORKDIR /app

COPY . .

RUN pip install poetry

RUN poetry config virtualenvs.in-project false
RUN poetry install --no-root
