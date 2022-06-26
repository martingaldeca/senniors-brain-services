#! /bin/sh

set -e
set -u
set -x

umask 000 # setting broad permissions to share log volume

pip install setuptools==59.6.0 # TODO remove when problem with dependencies fixed
celery -A celery_brain_services flower --port=5555