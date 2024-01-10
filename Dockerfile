from python:3.12.1-slim as base

WORKDIR /app

RUN pip install poetry==1.6.1

COPY --chmod=0755 pyproject.toml poetry.lock /app

ARG IS_DEBUG

RUN if [ "$IS_DEBUG" = "true" ] ; then \
        poetry export --with dev -f requirements.txt --output requirements.txt; \
    else \
        poetry export -f requirements.txt --output requirements.txt; \
    fi

RUN pip install -r requirements.txt

FROM python:3.12.1-slim

COPY --from=base /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/

COPY --from=base /usr/local/bin/ /usr/local/bin/

COPY . /app

WORKDIR /app

ENV PYTHONUNBUFFERED 1
