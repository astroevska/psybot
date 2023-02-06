FROM python:3.8-slim AS bot

ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONHASHSEED=random
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100

ENV TELEGRAM_TOKEN t123456789
ENV MONGODB_CONNECTION mongodb123456789

RUN apt-get update
RUN apt-get install -y python3 python3-pip python-dev build-essential python3-venv

RUN mkdir -p /codebase
ADD . /codebase
WORKDIR /codebase

RUN pip3 install -r requirements.txt
RUN chmod +x /codebase/main.py

CMD python3 /codebase/main.py;
