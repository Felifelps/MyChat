FROM python:3.11.5-slim-bookworm

RUN python3 -m venv venv

RUN  . ./venv/bin/activate && pip install --upgrade pip && pip install poetry

# Copy only requirements to cache them in docker layer
WORKDIR /code

COPY poetry.lock pyproject.toml /code/

# Project initialization:
RUN poetry install --no-root

# Creating folders, and files for a project:
COPY . /code

CMD ["python", "manage.py", "runserver"]