# app/Dockerfile
# pull the official docker image
FROM python:3.10.9-slim

# set work directory
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy project
COPY . .

# install dependencies
RUN apt-get update && apt-get install -y \
    bash    \
    cron    \
    gcc \
    libpq-dev   \
    musl-dev    \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install -r requirements.txt --no-cache-dir

# schedule etl using cron
RUN chmod 755 ./etl.sh ./entry.sh
RUN /usr/bin/crontab ./crontab.txt
CMD ["entry.sh"]
