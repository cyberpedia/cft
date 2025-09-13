# backend.Dockerfile
# Use a Python slim base image for smaller size
FROM python:3.11-slim-bullseye

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE ctf_platform.settings

# Set working directory inside the container
WORKDIR /app

# Install system dependencies needed for PostgreSQL client and Pillow
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project code
COPY . /app/

# Create a non-privileged user
RUN adduser --system --group ctfuser
USER ctfuser

# Expose the port your application will run on
EXPOSE 8000

# Command to run the ASGI server (Daphne)
# Django collects static files into STATIC_ROOT by default.
# python manage.py collectstatic --noinput should be run before deployment.
# For Docker, this could be done in docker-compose.yml or a separate entrypoint script.
# For simplicity, we'll run it in docker-compose.yml during startup.
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "ctf_platform.asgi:application"]
