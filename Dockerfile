FROM python:3.9-slim-buster

RUN mkdir -p /home/app
RUN addgroup --system app && adduser --system --group app
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

ARG LMS_ENV
ENV LMS_ENV=${LMS_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.1.6

RUN pip install "poetry==$POETRY_VERSION"

COPY poetry.lock pyproject.toml $APP_HOME

RUN poetry config virtualenvs.create false \
  && poetry install $(test "$LMS_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

COPY . $APP_HOME

RUN chown -R app:app $APP_HOME

USER app

CMD gunicorn config.wsgi:application --bind 0.0.0.0:$PORT