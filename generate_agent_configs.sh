#!/bin/bash
# Generate AgentCore config files for different agents
# Usage: ./generate_agent_configs.sh

WORKSHOP_DIR="/home/ubuntu/workshop/tdfsiworkshop"

# List of agents
declare -A AGENTS=(
    ["agent"]="agent.py"
    ["customer_retention"]="customer_retention_agent.py"
    ["credit_risk"]="credit_risk_agent.py"
    ["wealth_management"]="wealth_management_agent.py"
)

echo "📁 Generating AgentCore config files..."
echo ""

for name in "${!AGENTS[@]}"; do
    file="${AGENTS[$name]}"
    config_file="bedrock_agentcore.${name}.yaml"
    
    cat > "$config_file" << EOF
default_agent: agent
agents:
  agent:
    name: tdworkshop
    entrypoint: ${WORKSHOP_DIR}/${file}
    deployment_type: container
    platform: linux/arm64
    source_path: ${WORKSHOP_DIR}
    aws:
      execution_role_auto_create: true
      ecr_auto_create: true
      region: us-east-1
      network_configuration:
        network_mode: PUBLIC
      observability:
        enabled: true
    memory:
      mode: NO_MEMORY
EOF
    
    echo "✅ Created: $config_file"
done

echo ""
echo "=========================================="
echo "📋 To switch agents:"
echo ""
echo "1. Copy the config you want:"
echo "   cp bedrock_agentcore.customer_retention.yaml .bedrock_agentcore.yaml"
echo ""
echo "2. Deploy:"
echo "   agentcore deploy --auto-update-on-conflict"
echo ""
echo "Available configs:"
ls -1 bedrock_agentcore.*.yaml
echo "=========================================="
