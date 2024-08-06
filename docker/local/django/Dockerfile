## ARG and Base Image
ARG PYTHON_VERSION=3.11.2-bullseye
FROM python:${PYTHON_VERSION} as python

## Build Stage
FROM python as python-build-stage
ARG BUILD_ENVIRONMENT=local

# update package and build tools & PostgreSQL client libraries.
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev

COPY ./requirements .

# create python wheel packages for the dependencies listed in txt file.
RUN pip wheel --wheel-dir /usr/src/app/wheels \
    -r ${BUILD_ENVIRONMENT}.txt


## Run Stage
FROM python as python-run-stage
ARG BUILD_ENVIRONMENT=local

ARG APP_HOME=/app

# prevents Python from writing .pyc files to disk.
ENV PYTHONDONTWRITEBYTECODE 1

# ensures that Python output is sent straight to the terminal (unbuffered).
ENV PYTHONUNBUFFERED 1

ENV BUILD_ENV ${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

# installs the necessary runtime dependencies, purges unnecessary packages, and cleans up the package lists to keep the image small.
RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq-dev \
    gettext \
    && apt-get purge -y --auto-remove -o API::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

# copies the built wheel files from the python-build-stage stage to the current stage.    
COPY --from=python-build-stage /usr/src/app/wheels /wheels/

RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
    && rm -rf /wheels/

# copies the entrypoint script to the container.
COPY ./docker/local/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

# copies the start script to the container.
COPY ./docker/local/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

# copies the entire application code to the working directory in the container.
COPY . ${APP_HOME}

#  This sets the entrypoint script to be executed when the container starts.
ENTRYPOINT [ "/entrypoint" ]
