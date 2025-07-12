#!/bin/bash

# Description:
# This script forcefully stops and removes all Docker containers, volumes,
# networks, and images defined in the production Compose file.
# Provides a clean slate for production rebuild.

set -e  # Exit on error

# Resolve the script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Change to project root
cd "$PROJECT_ROOT"

echo "📁 Working in project: ${COMPOSE_PROJECT_NAME:-flask_template}"

echo "🛑 Stopping and removing containers, networks, and volumes..."
docker compose -f compose.yaml down --volumes --remove-orphans

VOLUME_NAME="${COMPOSE_PROJECT_NAME:-flask_template}_db-prod"
echo "🗑️ Removing production database volume: $VOLUME_NAME"
docker volume inspect "$VOLUME_NAME" > /dev/null 2>&1 && docker volume rm "$VOLUME_NAME" > /dev/null && echo "✔ Volume $VOLUME_NAME removed" || echo "ℹ️ Volume $VOLUME_NAME not found, skipping"


echo "🧹 Pruning dangling images and unused volumes..."
docker image prune -f
docker volume prune -f

echo "✅ Production Docker environment fully reset."
