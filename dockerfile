FROM python:3.11

SHELL ["/bin/bash", "-c"]

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN apt update

RUN useradd -rms /bin/bash web && chmod 777 /opt /run

WORKDIR /nearest-trucks-transportation


COPY --chown=nearest-trucks-transportation:nearest-trucks-transportation . .

RUN pip install -r requirements.txt

USER web

