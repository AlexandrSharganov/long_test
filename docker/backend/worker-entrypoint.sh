#!/bin/sh

until cd /app/long
do
    echo "Waiting for server volume..."
done

celery -A long worker --loglevel DEBUG --concurrency 1 -E
