# Minimal Dockerfile for Flask
# - Uses python slim image
# - Installs requirements
# - Runs app.py

FROM python:3.12-slim

# Avoid writing .pyc, enable unbuffered logs (nicer for CI logs)
ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1     PORT=8080

WORKDIR /app

# Install dependencies first (better cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY app.py .

EXPOSE 8080

# Run Flask app
CMD ["python", "app.py"]
