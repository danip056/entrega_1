FROM python:3.10-slim  AS base_python
WORKDIR /usr/src/dsc_app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip

RUN mkdir -p /usr/share/man/man1/ && \
	apt-get update && apt-get install -y \
	build-essential && \
	apt-get clean;

FROM base_python as app
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./ ./
