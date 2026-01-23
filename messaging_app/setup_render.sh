#!/bin/bash
# setup_render.sh

echo "Setting up for Render deployment..."

# Create production settings
cp messaging_app/settings.py messaging_app/settings_prod.py

# Update Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=messaging_app.settings_prod

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

COPY . .

RUN python manage.py collectstatic --noinput

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "messaging_app.wsgi:application"]
EOF

# Create render.yaml
cat > render.yaml << 'EOF'
services:
  - type: web
    name: messaging-app
    env: docker
    dockerfilePath: ./Dockerfile
    dockerContext: .
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: messaging-db
          property: connectionString
      - key: SECRET_KEY
        generateValue: true
      - key: DJANGO_SETTINGS_MODULE
        value: messaging_app.settings_prod
      - key: ALLOWED_HOSTS
        value: messaging-app.onrender.com,localhost,127.0.0.1
      - key: DEBUG
        value: "False"
    healthCheckPath: /api/schema/swagger-ui/
    autoDeploy: true
    plan: free
    numInstances: 1

databases:
  - name: messaging-db
    plan: free
    databaseName: messaging_app
    user: messaging_user
EOF

echo "Setup complete! Files created:"
echo "- Dockerfile (updated)"
echo "- render.yaml"
echo "- messaging_app/settings_prod.py"
echo ""
echo "Next steps:"
echo "1. git add ."
echo "2. git commit -m 'Prepare for Render'"
echo "3. git push origin main"
echo "4. Go to Render.com → New Blueprint → Connect repo"
