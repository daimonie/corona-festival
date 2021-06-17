FROM python:3.8-slim

COPY container/ /opt/container
WORKDIR /opt/container

RUN pip install --no-cache-dir -r /opt/container/requirements.txt
RUN echo 'deb http://deb.debian.org/debian testing main' >> /etc/apt/sources.list \
    && apt-get update && apt-get install -y --no-install-recommends -o APT::Immediate-Configure=false gcc g++