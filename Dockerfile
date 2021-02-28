FROM python:3.9-buster as base
EXPOSE 5000
RUN pip install poetry
RUN mkdir /app
WORKDIR /app

COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false --local && poetry install --no-root --no-dev

COPY . /app/

FROM base as production
ENV FLASK_ENV=production
CMD gunicorn --bind 0.0.0.0:$PORT 'moot_app.app:create_app()'

FROM base as development
ENTRYPOINT ["poetry", "run", "flask", "run", "--host", "0.0.0.0"]