FROM python:3.9.7-slim-bullseye

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
  # packages to build other Python packages
  && apt-get install -y build-essential \
  # postgres requirements
  && apt-get install -y libpq-dev \
  # ffmpeg
  && apt-get install -y ffmpeg \
  # socat, strictly fo dev purposes to make keycloak available locally
  # ========= DON'T USE IN PRODUCTION =========
  && apt-get install -y socat \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# app entrypoint
COPY ./docker/app/dev/entrypoint.sh /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

RUN mkdir -p /data/media

# install requirements here to make sure they are cached
COPY ./requirements /requirements
RUN pip install -r /requirements/dev.txt

WORKDIR /app
ENTRYPOINT ["/entrypoint"]
