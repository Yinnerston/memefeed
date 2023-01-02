# app/Dockerfile

# pull the official docker image
FROM python:3.10.9-alpine

# set work directory
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
# copy project
COPY . .

RUN apk add --update apk-cron && rm -rf /var/cache/apk/*
RUN apk update && apk add bash
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

# schedule etl using cron
RUN chmod 755 ./etl.sh ./entry.sh
RUN /usr/bin/crontab ./crontab.txt
CMD ["entry.sh"]
