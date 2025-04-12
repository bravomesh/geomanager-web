# --------- requirements ---------
ARG GDAL_VERSION=3.7.0
FROM ghcr.io/osgeo/gdal:ubuntu-small-${GDAL_VERSION} AS builder

RUN apt-get update && apt-get install -y cron git libgeos-dev python3-pip --fix-missing

WORKDIR /tmp

RUN pip install poetry poetry-plugin-export

COPY ./pyproject.toml ./poetry.lock* ./README.md /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


# syntax = docker/dockerfile:1.5

# use osgeo gdal ubuntu small 3.7 image.
# pre-installed with GDAL 3.7.0 and Python 3.10.6
ARG GDAL_VERSION=3.7.0
FROM ghcr.io/osgeo/gdal:ubuntu-small-${GDAL_VERSION} AS runnner

# install dependencies
RUN apt-get update && apt-get install -y \
    cron \
    git \
    libgeos-dev \
    imagemagick \
    libmagic1 \
    libcairo2-dev \
    libffi-dev \
    python3-pip --fix-missing \
    lsb-release

# for pg_dump
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
    && cat /etc/apt/sources.list.d/pgdg.list \
    && curl --silent https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
    && apt-get update \
    && apt-get install -y postgresql-client-15

# set python env
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

# install docker-compose wait
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.12.0/wait /wait
RUN chmod +x /wait

# create app home dir
ENV APP_HOME=/home/app
RUN mkdir -p $APP_HOME

# setup working dir
WORKDIR $APP_HOME

# copy requirements
COPY --from=builder /tmp/requirements.txt ${APP_HOME}

# install requirements
RUN --mount=type=cache,target=/root/.cache  \
    pip install --upgrade pip \
    && pip install gunicorn \
    && pip install uvicorn \
    && pip install -r requirements.txt

# copy code
COPY . $APP_HOME

# create autoingestion directory
ENV GEOMANAGER_AUTO_INGEST_RASTER_DATA_DIR=/geomanager/data
RUN mkdir -p $GEOMANAGER_AUTO_INGEST_RASTER_DATA_DIR

# copy entrypoint.sh
COPY ./docker/cms/docker-entrypoint.sh ./
RUN chmod +x docker-entrypoint.sh

## add backup.cron to crontab
#COPY ./docker/cms/backup.cron /etc/cron.d/backup.cron
#RUN chmod 0644 /etc/cron.d/backup.cron && crontab /etc/cron.d/backup.cron

# create tmp dir for handling large django uploads
RUN mkdir -p tmp

# Port used by this container to serve HTTP.
EXPOSE 8000