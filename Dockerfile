FROM python:3.11.5-slim-bookworm

RUN python3 -m venv venv

RUN source venv/bin/activate

RUN pip install poetry

# Copy only requirements to cache them in docker layer
WORKDIR /code

COPY poetry.lock pyproject.toml /code/

# Project initialization:
RUN poetry install --no-root --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY . /code

CMD ["python", "manage.py", "runserver"]