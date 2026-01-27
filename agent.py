#!/usr/bin/env python3
"""
Teradata Workshop Agent
Connects to shared Teradata cluster via MCP and provides AI-powered banking analytics.

Configuration via .env file:
- TERADATA_DATABASE_URI: Connection string to Teradata cluster

AWS credentials come from EC2 IAM role automatically.
"""

import os
from dotenv import load_dotenv

# Load .env file BEFORE reading environment variables
load_dotenv()

from strands import Agent
from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters
from strands.models.bedrock import BedrockModel
from bedrock_agentcore.runtime import BedrockAgentCoreApp

# Get database URI from environment (.env file)
database_uri = os.getenv("TERADATA_DATABASE_URI")
if not database_uri:
    raise ValueError(
        "TERADATA_DATABASE_URI environment variable is required.\n"
        "Check your .env file or run: cat .env"
    )

# MCP Server configuration
teradata_config = {
    "command": "uvx",
    "args": ["teradata-mcp-server"],
    "env": {
        "DATABASE_URI": database_uri
    }
}

# Model configuration
MODEL_ID = "anthropic.claude-3-5-sonnet-20240620-v1:0"

# Create model and MCP client
model = BedrockModel(model_id=MODEL_ID, streaming=False)

server_params = StdioServerParameters(
    command=teradata_config["command"],
    args=teradata_config["args"],
    env=teradata_config["env"]
)

teradata_tool = MCPClient(lambda: stdio_client(server_params))

# AgentCore app
app = BedrockAgentCoreApp()

@app.entrypoint
def invoke(payload):
    """AgentCore entry point"""
    
    system_prompt = """You are a Banking Data Analyst with direct access to a Teradata database 
containing customer data for a European bank.

**Available Data:**
- 10,000 customers across France, Germany, and Spain
- Customer demographics, balances, credit scores
- Product usage and activity status
- Churn indicators

**Your Capabilities:**
- Query customer data using SQL via the Teradata MCP tool
- Analyze patterns in customer behavior
- Identify risks and opportunities
- Provide actionable business insights

**Guidelines:**
- Always show sample data (first 5-10 rows) to support your analysis
- Calculate relevant metrics and statistics
- Provide clear, actionable recommendations
- Be specific with numbers and percentages

Start by understanding what databases and tables are available, then help the user analyze their data."""

    agent = Agent(
        model=model,
        tools=[teradata_tool],
        system_prompt=system_prompt
    )
    
    user_message = payload.get("prompt", "What databases and tables are available?")
    result = agent(user_message)
    return {"response": result.message}


def interactive_mode():
    """Run agent in interactive REPL mode (for local testing)"""
    
    print("=" * 60)
    print("Teradata Workshop Agent - Interactive Mode")
    print("=" * 60)
    
    # Show connection info (hide password)
    uri_display = database_uri.split('@')[1] if '@' in database_uri else database_uri
    print(f"Connected to: {uri_display}")
    print("Type 'quit' or 'exit' to stop")
    print("=" * 60)
    print()
    
    system_prompt = """You are a Banking Data Analyst with access to Teradata.
Help users query and analyze customer banking data.
Show sample data to support your analysis."""

    agent = Agent(
        model=model,
        tools=[teradata_tool],
        system_prompt=system_prompt
    )
    
    while True:
        try:
            query = input("You: ").strip()
            if query.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            if not query:
                continue
                
            print("\nAgent: Thinking...\n")
            result = agent(query)
            print(f"Agent: {result.message}\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        # Run in interactive mode for local testing
        interactive_mode()
    else:
        # Run as AgentCore service
        app.run()