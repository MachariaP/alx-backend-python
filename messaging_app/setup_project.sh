#!/bin/bash

echo "Setting up Docker for Django Messaging App..."

# Find project root (where manage.py is)
MANAGE_PATH=$(find . -name "manage.py" -type f | head -1)
if [ -z "$MANAGE_PATH" ]; then
    echo "Error: manage.py not found!"
    exit 1
fi

PROJECT_ROOT=$(dirname "$MANAGE_PATH")
echo "Project root found at: $PROJECT_ROOT"

# Navigate to project root
cd "$PROJECT_ROOT"
echo "Current directory: $(pwd)"

# Create requirements.txt if doesn't exist
if [ ! -f "requirements.txt" ]; then
    echo "Creating requirements.txt..."
    cat > requirements.txt << 'REQ_EOF'
Django==4.2.0
mysqlclient==2.2.0
djangorestframework==3.14.0
django-cors-headers==4.0.0
python-decouple==3.8
REQ_EOF
fi

# Create Dockerfile
echo "Creating Dockerfile..."
cat > Dockerfile << 'DOCKER_EOF'
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
DOCKER_EOF

# Create docker-compose.yml
echo "Creating docker-compose.yml..."
cat > docker-compose.yml << 'COMPOSE_EOF'
version: '3.8'

services:
  db:
    image: mysql:8.0
    container_name: messaging_db
    restart: unless-stopped
    environment:
      MYSQL_DATABASE: ${MYSQL_DATABASE}
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
    ports:
      - "3307:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    networks:
      - messaging_network

  web:
    build: .
    container_name: messaging_web
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      MYSQL_DATABASE: ${MYSQL_DATABASE}
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
      MYSQL_HOST: db
      MYSQL_PORT: 3306
      DJANGO_SECRET_KEY: ${DJANGO_SECRET_KEY}
      DJANGO_DEBUG: ${DJANGO_DEBUG}
      DJANGO_ALLOWED_HOSTS: ${DJANGO_ALLOWED_HOSTS}
    depends_on:
      - db
    volumes:
      - .:/app
    networks:
      - messaging_network
    command: >
      sh -c "python manage.py migrate &&
             python manage.py runserver 0.0.0.0:8000"

volumes:
  mysql_data:
    driver: local

networks:
  messaging_network:
    driver: bridge
COMPOSE_EOF

# Create .env file
echo "Creating .env file..."
cat > .env << 'ENV_EOF'
MYSQL_DATABASE=messaging_db
MYSQL_USER=app_user
MYSQL_PASSWORD=secure_password_123
MYSQL_ROOT_PASSWORD=root_password_456
DJANGO_SECRET_KEY=django-insecure-3!4j$v8&*m^g#h@k%lz
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
ENV_EOF

echo "Setup complete!"
echo ""
echo "To start the application, run: docker-compose up --build"
echo "The app will be available at: http://localhost:8000"
