# Use an official Python runtime as a parent image
FROM python:3.11.5-slim-bookworm

# Set the working directory in the container to /app
WORKDIR /code

# Add the current directory contents into the container at /app
ADD . /code

# Install any needed packages specified in requirements.txt
RUN python3 -m venv venv \
    && . ./venv/bin/activate \
    && pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root \
    && poetry shell


# Make port 80 available to the world outside this container
EXPOSE 8000

# Run manage.py when the container launches
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]