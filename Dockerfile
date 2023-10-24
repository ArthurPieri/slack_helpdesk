# Use an official Python runtime as a parent image
FROM python:3.12.0-slim

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install curl, gcc and python3-dev
# RUN apk add --no-cache curl
RUN apt-get -y update && apt-get -y install curl


# Install poetry and configure it
RUN curl -sSL https://install.python-poetry.org | python - && \
    /root/.local/bin/poetry config virtualenvs.create false

# Install dependencies
RUN /root/.local/bin/poetry install --only=main --no-cache

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Run your bot when the container launches
CMD ["python", "src/app.py"]
