#!/bin/bash

# Description:
# This script forcefully stops and removes all Docker containers, volumes,
# networks, and images defined in the development Compose files.
# It gives a clean slate for rebuilding everything.

set -e  # Exit on error

# Resolve the script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Change to project root
cd "$PROJECT_ROOT"

echo "🛑 Stopping and removing containers, networks, and volumes..."
docker compose -f compose.yaml -f docker-compose.override.yaml down --volumes --remove-orphans

echo "🧹 Pruning dangling images and unused volumes..."
docker image prune -f
docker volume prune -f

echo "✅ Docker environment fully reset."
