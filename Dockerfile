FROM python:3.11.5-slim-bookworm

RUN python3 -m venv venv

WORKDIR /code

COPY poetry.lock pyproject.toml /code/

RUN  . ./venv/bin/activate && pip install --upgrade pip && pip install poetry && poetry install --no-root

COPY . /code

CMD ["python", "manage.py", "runserver"]