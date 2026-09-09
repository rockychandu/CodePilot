# CodePilot Enterprise Multi-Language Production Container
FROM python:3.12-slim

# Install system utilities, build tools, GCC, G++, Node.js, and OpenJDK
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    nodejs \
    npm \
    default-jdk \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY backend/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

# Expose API port (5000) and Web port (8000)
EXPOSE 5000 8000

ENV PORT=5000
ENV ENV=production
ENV PYTHONUNBUFFERED=1

CMD ["python", "backend/app.py"]
