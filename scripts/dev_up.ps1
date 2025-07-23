# Description:
# This script builds and starts the development Docker environment
# using compose.yaml and docker-compose.override.yaml from the project root.

# Ensure errors stop execution
$ErrorActionPreference = "Stop"

# Resolve the script directory and project root
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectRoot = Split-Path -Parent $ScriptDir

# Change to the project root directory.
Set-Location $ProjectRoot

Write-Host "🔧 Building Docker images without cache..."
docker compose -f compose.yaml -f docker-compose.override.yaml build --no-cache

Write-Host "🚀 Starting containers in detached mode..."
docker compose -f compose.yaml -f docker-compose.override.yaml up -d

Write-Host "✅ Development environment is up and running."