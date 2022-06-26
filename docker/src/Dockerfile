FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Set the external and internal path for the docker container
ARG PROJECT_EXTERNAL_PATH=src/
ARG PROJECT_INTERNAL_PATH=/app/src

#Load source code from the repository or local to the container
COPY ${PROJECT_EXTERNAL_PATH}/ /app/src

# Prepare work directory
RUN mkdir -p src
WORKDIR src

# Install all the requirements
RUN pip install poetry
ADD ${PROJECT_EXTERNAL_PATH}/poetry.lock ${PROJECT_INTERNAL_PATH}
ADD ${PROJECT_EXTERNAL_PATH}/pyproject.toml ${PROJECT_INTERNAL_PATH}
RUN poetry config virtualenvs.create false && poetry install

# Load executors
ADD docker/src/post_deploy.sh /run_scripts/post_deploy.sh
ADD docker/src/run_worker.sh /run_scripts/run_worker.sh
ADD docker/src/run_beat.sh /run_scripts/run_beat.sh
ADD docker/src/run_flower.sh /run_scripts/run_flower.sh

# Ipython config
RUN mkdir -p /root/.ipython/profile_default/
ADD docker/src/ipython_config.py /root/.ipython/profile_default/ipython_config.py
