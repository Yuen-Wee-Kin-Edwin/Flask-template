#!/bin/bash

# Description:
# This script builds and starts the development Docker environment
# using compose.yaml and docker-compose.override.yaml from the project root.

set -e  # Exit immediately on error

# Resolve the script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Change to project root
cd "$PROJECT_ROOT"

echo "🔧 Building Docker images without cache..."
docker compose -f compose.yaml -f docker-compose.override.yaml build --no-cache

echo "🚀 Starting containers in detached mode..."
docker compose -f compose.yaml -f docker-compose.override.yaml up -d

echo "✅ Development environment is up and running."
