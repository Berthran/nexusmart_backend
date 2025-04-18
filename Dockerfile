# Dockerfile for NexusMart Django Application

# --- Base Image ---
# Start with an official Python runtime as a parent image.
# Using 'slim' version for a smaller image size. Choose a specific version for reproducibility.
FROM python:3.11-slim

# --- Environment Variables ---
# Set environment variables to prevent Python from writing pyc files to disc (improves performance in Docker).
# and prevent Python from buffering stdout and stderr (makes logs appear immediately).
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# --- System Dependencies ---
# Install system dependencies required by Django and psycopg2 (PostgresSQL adapter)
# 'build-essential' provides tools needed to compile some Python packages.
# 'libpq-dev' provides header files needed to build psycopg2.
# We update apt-get, install dependencies, then clean up apt cache to keep the image small.
RUN apt-get update \ 
    && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# --- Application Setup ---
# Set the working directory inside the container. All subsequent comands (RUN, CMD, COPY, etc.)
# will be executed relative to this directory
WORKDIR /app

# --- Python Dependencies ---
# Copy the requirements file into the container first.
# This leverages Docker's layer caching. If requirements.txt doesn't change,
# Docker can reuse the layer where dependencies were installed, speeding up builds
COPY ./requirements.txt /app/requirements.txt

# Install Python dependencies specified in requirements.txt
# Using --no-cache-dir prevents pip from storing downloaded packages, keeping the image smaller.
RUN pip install --no-cache-dir -r requirements.txt

# --- Copy Application Code ---
# Copy the rest of the application code from your local machine into the container's working directory (/app).
# This should come *after* installing dependencies to optimize Docker layer caching
COPY . /app/

# --- Default Command ---
# (Optional for development, as docker-compose will override this command)
# Specifies the default command to run when a container is started from this image
# For production, this might be gunicorn or uvicorn.
# CMD ["gunicorn", "nexustmart_config.wsgi:application", "--bing", "0.0.0.0:8000"]