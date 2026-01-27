#!/bin/bash
# setup_agentcore.sh
# Run this inside /home/ubuntu/workshop/tdmcpagentcore
# Creates all required files for AgentCore deployment
#
# Usage:
#   ./setup_agentcore.sh
#   ./setup_agentcore.sh "teradata://user:pass@host:1025/db"

set -e

WORKSHOP_DIR=$(pwd)

echo "🔧 Setting up AgentCore in: $WORKSHOP_DIR"
echo ""

# Get Teradata URI from argument or prompt
if [ -n "$1" ]; then
    TERADATA_URI="$1"
    echo "📊 Using Teradata URI from argument"
else
    echo "📊 Enter Teradata connection string"
    echo "   Format: teradata://user:password@host:port/database"
    echo "   Example: teradata://xxx:yyy@11.111.185.194:1025/BankingDB"
    echo ""
    read -p "   TERADATA_DATABASE_URI: " TERADATA_URI
fi

if [ -z "$TERADATA_URI" ]; then
    echo "❌ Error: Teradata URI is required"
    exit 1
fi

echo "   URI: $TERADATA_URI"
echo ""

# Get AWS account ID from IAM role
echo "📡 Getting AWS account info..."
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REGION="us-east-1"
echo "   Account ID: $ACCOUNT_ID"
echo "   Region: $REGION"
echo ""

# 1. Create .env file (for local testing)
echo "📝 Creating .env file..."
cat > .env << ENV_END
# Teradata Workshop Configuration
TERADATA_DATABASE_URI=${TERADATA_URI}
AWS_DEFAULT_REGION=us-east-1
ENV_END
echo "   ✅ .env created"

# 2. Create requirements_linux.txt
echo "📝 Creating requirements_linux.txt..."
cat > requirements_linux.txt << 'REQ_END'
strands-agents>=1.19.0
mcp>=1.22.0
boto3
bedrock-agentcore>=1.1.1
python-dotenv
streamlit
REQ_END
echo "   ✅ requirements_linux.txt created"

# 3. Create Dockerfile WITH TERADATA_DATABASE_URI baked in
echo "📝 Creating Dockerfile..."
cat > Dockerfile << DOCKER_END
# Teradata Workshop - AgentCore Container
FROM --platform=linux/arm64 ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements_linux.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install aws-opentelemetry-distro==0.12.2

# Copy application code
COPY . .

# Set environment variables - TERADATA_URI baked in at build time
ENV PYTHONUNBUFFERED=1
ENV AWS_REGION=us-east-1
ENV TERADATA_DATABASE_URI=${TERADATA_URI}

# Expose port
EXPOSE 8080

# Run the application
CMD ["opentelemetry-instrument", "python", "agent.py"]
DOCKER_END
echo "   ✅ Dockerfile created (with TERADATA_DATABASE_URI)"

# 4. Create .bedrock_agentcore.yaml
echo "📝 Creating .bedrock_agentcore.yaml..."
cat > .bedrock_agentcore.yaml << YAML_END
default_agent: agent
agents:
  agent:
    name: tdworkshop
    entrypoint: ${WORKSHOP_DIR}/agent.py
    deployment_type: container
    platform: linux/arm64
    source_path: ${WORKSHOP_DIR}
    aws:
      execution_role_auto_create: true
      account: '${ACCOUNT_ID}'
      region: ${REGION}
      ecr_auto_create: true
      s3_auto_create: true
      network_configuration:
        network_mode: PUBLIC
      observability:
        enabled: true
    memory:
      mode: NO_MEMORY
YAML_END
echo "   ✅ .bedrock_agentcore.yaml created"

# 5. Check if agent.py has load_dotenv
if ! grep -q "load_dotenv" agent.py 2>/dev/null; then
    echo "⚠️  Note: agent.py may need 'from dotenv import load_dotenv' and 'load_dotenv()' at top for local testing"
fi

echo ""
echo "=============================================="
echo "✅ Setup complete!"
echo "=============================================="
echo ""
echo "Configuration:"
echo "  - Teradata: ${TERADATA_URI}"
echo "  - AWS Account: ${ACCOUNT_ID}"
echo "  - Region: ${REGION}"
echo ""
echo "Files created:"
echo "  - .env (local testing)"
echo "  - .bedrock_agentcore.yaml (AgentCore config)"
echo "  - Dockerfile (with TERADATA_DATABASE_URI baked in)"
echo "  - requirements_linux.txt (dependencies)"
echo ""
echo "Next steps:"
echo "  1. Run: agentcore deploy --auto-update-on-conflict"
echo "  2. Test: agentcore invoke '{\"prompt\": \"What tables are available?\"}'"
echo ""