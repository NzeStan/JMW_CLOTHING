#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status

# Log function with timestamps
log() {
    echo "$(date +'%Y-%m-%d %H:%M:%S') - $1"
}

log "Starting script execution..."

# Load environment variables from the specified .env file
if [ -f "$ENV_FILE" ]; then
    export $(grep -v '^#' "$ENV_FILE" | xargs)
fi

# Required environment variables
REQUIRED_VARS=("DJANGO_SECRET_KEY")
for var in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!var}" ]; then
        log "Error: $var is not set. Please check your environment configuration."
        exit 1
    fi
done

log "DJANGO_DEBUG: $DJANGO_DEBUG"

# Make and run migrations if enabled
if [ "${RUN_MIGRATIONS:-true}" = "true" ]; then
    log "Making migrations..."
    python manage.py makemigrations
    log "Running migrations..."
    python manage.py migrate
else
    log "Skipping migrations as per configuration."
fi

# Build Tailwind CSS in production mode
if [ "$DJANGO_DEBUG" != "True" ]; then
    log "Building Tailwind CSS..."
    cd theme/static_src && npm run build
    cd ../..
    log "Tailwind build completed successfully."

    log "Collecting static files..."
    python manage.py collectstatic --noinput
    log "Collectstatic completed successfully."
fi

# Start server based on environment
if [ "$DJANGO_DEBUG" = "True" ]; then
    log "Starting development server..."
    exec python manage.py runserver 0.0.0.0:8000
else
    log "Starting production server with Gunicorn..."
    exec gunicorn CLOTHING_JMW.wsgi:application --bind 0.0.0.0:8000
fi