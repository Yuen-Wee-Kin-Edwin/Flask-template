# Description:
# This script forcefully stops and removes all Docker containers, volumes,
# networks, and images defined in the development Compose files.
# It gives a clean slate for rebuilding everything.

# Exit on error
$ErrorActionPreference = "Stop"

# Resolve the script directory and project root
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectRoot = Split-Path -Parent $ScriptDir

# Change to project root
Set-Location $ProjectRoot

Write-Host "🛑 Stopping and removing containers, networks, and volumes..."
docker compose -f compose.yaml -f docker-compose.override.yaml down --volumes --remove-orphans

Write-Host "🧹 Pruning dangling images and unused volumes..."
docker image prune -f
docker volume prune -f

Write-Host "✅ Development Docker environment fully reset."
