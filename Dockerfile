# Pull base image
FROM python:3.10.4-slim-bullseye

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install the latest Node.js and npm
RUN apt-get update && \
    apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_current.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Install npm dependencies
WORKDIR /code/theme/static_src
RUN npm install

# Set final working directory
WORKDIR /code

# Expose port 8000
EXPOSE 8000

# Entry point
ENTRYPOINT ["/code/entrypoint.sh"]