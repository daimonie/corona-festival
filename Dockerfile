FROM python:3.8

COPY container/ /opt/container
WORKDIR /opt/container

RUN cat /opt/container/requirements.txt
RUN pip install --no-cache-dir -r /opt/container/requirements.txt