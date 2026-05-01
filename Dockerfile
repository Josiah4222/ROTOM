FROM python:3.11-slim

# Install system dependencies for Pillow and other packages
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Create directories for static and media files
RUN mkdir -p /var/www/rotom/staticfiles /var/www/rotom/media

# Collect static files
RUN python manage.py collectstatic --noinput

# Run as non-root user for security (UID 1000 matches host volume ownership)
RUN useradd -u 1000 -m appuser && chown -R appuser:appuser /app /var/www/rotom
USER appuser

# Expose port
EXPOSE 8000

# Start Gunicorn
CMD ["gunicorn", \
     "--workers", "3", \
     "--bind", "0.0.0.0:8000", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "REACHONEETH.wsgi:application"]
