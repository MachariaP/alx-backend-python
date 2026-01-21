#!/bin/bash

echo "Fixing Docker checks..."

# 1. Ensure Dockerfile has exact base image
cat > messaging_app/Dockerfile << 'DOCKER_EOF'
FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
DOCKER_EOF

# 2. Ensure requirements.txt exists
if [ ! -f "messaging_app/requirements.txt" ]; then
    cat > messaging_app/requirements.txt << 'REQ_EOF'
Django==4.2.0
mysqlclient==2.2.0
djangorestframework==3.14.0
django-cors-headers==4.0.0
python-decouple==3.8
REQ_EOF
fi

# 3. Verify the files
echo "=== Verification ==="
echo "Dockerfile contents (first few lines):"
head -20 messaging_app/Dockerfile
echo ""
echo "requirements.txt contents:"
cat messaging_app/requirements.txt
echo ""
echo "File sizes:"
ls -lh messaging_app/Dockerfile messaging_app/requirements.txt
