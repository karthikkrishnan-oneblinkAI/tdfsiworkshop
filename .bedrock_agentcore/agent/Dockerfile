# Use GitHub Container Registry to avoid Docker Hub rate limits
FROM --platform=linux/arm64 ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY minimal_requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install aws-opentelemetry-distro==0.12.2

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV AWS_REGION=us-east-1

# Expose port
EXPOSE 8080

# Run the application
CMD ["opentelemetry-instrument", "python", "agent.py"]
