FROM python:3.12-slim-bullseye

# SYSTEM ENV
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_CREATE False
ENV PATH="$POETRY_HOME/bin:$PATH"
ENV PYTHONPATH="/opt/app/bookstore"


RUN set -ex \
    && BUILD_DEPS=" \
    gcc \
    make \
    curl \
    wget \
    build-essential \
    python-dev \
    libpcre3-dev \
    libpq-dev" \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{} \
    && apt-get update && apt-get install -y --no-install-recommends $BUILD_DEPS \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python -

RUN mkdir -p \
    /opt/app/log \
    /opt/app/src \
    /opt/app/bin

COPY pyproject.toml poetry.lock alembic.ini /opt/app/

WORKDIR /opt/app

RUN poetry install --only main --no-interaction --no-root

COPY ./bookstore /opt/app/bookstore
COPY ./bin /opt/app/bin

RUN chmod -R +x /opt/app/bin

VOLUME '/opt/app/log'

EXPOSE 8000

ENTRYPOINT ["docker-entrypoint"]
CMD ["initial"]


