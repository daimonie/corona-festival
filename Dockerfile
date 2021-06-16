FROM python:3.8-slim

COPY container/ /opt/container
WORKDIR /opt/container

RUN pip install --no-cache-dir -r /opt/container/requirements.txt