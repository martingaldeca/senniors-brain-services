#! /bin/sh

set -e
set -u
set -x

umask 000 # setting broad permissions to share log volume

celery -A celery_brain_services worker --loglevel=$CELERY_LOG_LEVEL --logfile="/src/logs/$WORKER_NAME.log" --time-limit 86400 --concurrency $WORKER_CONCURRENCY -n $WORKER_NAME