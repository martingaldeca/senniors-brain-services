#!make
include .env
.DEFAULT_GOAL=up
MAKEFLAGS += --no-print-directory

# Constants
TAIL_LOGS = 50

up:
	$s docker-compose up -d

down:
	$s docker-compose down

down-up: down up

build:
	$s docker-compose build

up-build:
	$s docker-compose down
	$s docker-compose up -d --build

complete-build:
	$s docker image prune -af
	$s docker-compose build
	$s docker-compose down
	$s docker-compose up -d

logs:
	$s docker logs --tail ${TAIL_LOGS} -f ${PROJECT_NAME}_brain_services

bash:
	$s docker exec -it ${PROJECT_NAME}_brain_services bash

sh:
	$s docker exec -it ${PROJECT_NAME}_brain_services bash

shell:
	$s docker exec -it ${PROJECT_NAME}_brain_services ipython

test:
	$s docker exec ${PROJECT_NAME}_brain_services python -m pytest --log-cli-level=ERROR --disable-pytest-warnings

flake8:
	$s docker exec ${PROJECT_NAME}_brain_services flake8

update-requirements:
	$s docker exec ${PROJECT_NAME}_brain_services poetry update

all-logs:
	$s docker-compose logs --tail ${TAIL_LOGS} -f

worker-logs:
	$s docker exec -it ${PROJECT_NAME}_worker tail -f logs/default_worker.log

celery-logs:
	$s docker logs --tail ${TAIL_LOGS} -f ${PROJECT_NAME}_worker

beat-logs:
	$s docker logs --tail ${TAIL_LOGS} -f ${PROJECT_NAME}_beat

worker-bash:
	$s docker exec -it ${PROJECT_NAME}_worker bash