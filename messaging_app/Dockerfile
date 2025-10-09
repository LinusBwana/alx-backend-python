# Use Python 3.10 as base image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Copy dependency file into the container
COPY requirements.txt /app/

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies from requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app

# Collect static files (if applicable)
RUN python manage.py collectstatic --noinput --clear || true

# Expose port 8000 (default Django development server port)
EXPOSE 8000

# Run the Django application
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Run migrations and start server
CMD python manage.py migrate && \
    python manage.py runserver 0.0.0.0:8000 -p 8000