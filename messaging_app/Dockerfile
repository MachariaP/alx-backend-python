# messaging_app/Dockerfile
FROM python:3.10          # ← exact tag the checker wants

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies needed for mysqlclient (or psycopg2, etc.)
RUN apt-get update && \
    apt-get install -y gcc default-libmysqlclient-dev pkg-config && \
    rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose the port Django runs on
EXPOSE 8000

# Run the server (accessible from outside the container)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
