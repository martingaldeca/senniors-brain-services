#! /bin/sh

set -e
set -u
set -x

umask 000 # setting broad permissions to share log volume

celery -A celery_brain_services beat --loglevel=$CELERY_LOG_LEVEL --logfile="/src/logs/$WORKER_NAME.log"