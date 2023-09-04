FROM python:3.8.10-alpine

RUN apk update && apk add python3-dev gcc libc-dev

WORKDIR /app
ADD ./requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install gunicorn
RUN apk add libffi-dev
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

ADD ./long /app/long
ADD ./docker /app/docker

RUN chmod +x /app/docker/backend/server-entrypoint.sh
RUN chmod +x /app/docker/backend/worker-entrypoint.sh
