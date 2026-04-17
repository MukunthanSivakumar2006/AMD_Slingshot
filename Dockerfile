# ── Stage 1: Use official slim Python image ──────────────────────────────────
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy dependency list first (so Docker caches this layer)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Cloud Run injects the PORT env variable (default 8080)
# Gunicorn will bind to it
ENV PORT=8080

# Expose the port (documentation only — Cloud Run reads PORT env var)
EXPOSE 8080

# Start the app with Gunicorn (production-grade WSGI server)
# 1 worker is fine for a prototype; scale workers for production
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 60 app:app
