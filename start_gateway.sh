#!/bin/bash

# Load environment variables from .env file
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
else
  echo ".env file not found!"
  exit 1
fi

# export MCP_BEARER_TOKEN=$(python3 -m mcpgateway.utils.create_jwt_token --username admin --exp 0 --secret my-test-key)

# Run the command
mcpgateway --host 0.0.0.0 --port 4444


