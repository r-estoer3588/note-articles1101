# n8n Notes Organizer - Startup Script
# Settings are permanently saved, just run this script

Write-Host 'Starting n8n Notes Organizer...' -ForegroundColor Green

# Move to script directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# Check if Docker is running
$null = docker info 2>$null
if (-not $?) {
    Write-Host 'ERROR: Docker is not running' -ForegroundColor Red
    Write-Host '  Please start Docker Desktop and try again' -ForegroundColor Yellow
    exit 1
}

# Check if docker-compose.yml exists
if (-not (Test-Path 'docker-compose.yml')) {
    Write-Host 'ERROR: docker-compose.yml not found' -ForegroundColor Red
    Write-Host '  Please run this script in the workflows/ directory' -ForegroundColor Yellow
    exit 1
}

# Start n8n container
Write-Host 'Starting n8n container...' -ForegroundColor Cyan
docker-compose up -d

if ($LASTEXITCODE -eq 0) {
    Write-Host ''
    Write-Host 'n8n started successfully!' -ForegroundColor Green
    Write-Host ''
    Write-Host 'Open in browser:' -ForegroundColor White
    Write-Host '  http://localhost:5678' -ForegroundColor Yellow
    Write-Host ''
    Write-Host 'Login credentials:' -ForegroundColor White
    Write-Host '  Username: admin' -ForegroundColor Yellow
    Write-Host '  Password: Check docker-compose.yml' -ForegroundColor Yellow
    Write-Host ''
    Write-Host 'First time setup only:' -ForegroundColor White
    Write-Host '  1. Import notes-to-notion-auto-organizer.json' -ForegroundColor Cyan
    Write-Host '  2. Configure OpenAI/Notion API keys' -ForegroundColor Cyan
    Write-Host '  3. Activate the workflow' -ForegroundColor Cyan
    Write-Host ''
    Write-Host 'After setup, no configuration needed!' -ForegroundColor Green
    Write-Host ''
    
    # Ask if user wants to see logs
    Write-Host 'Show logs? (y/N): ' -NoNewline -ForegroundColor White
    $response = Read-Host
    if ($response -eq 'y' -or $response -eq 'Y') {
        docker-compose logs -f n8n
    }
} else {
    Write-Host ''
    Write-Host 'ERROR: Failed to start n8n' -ForegroundColor Red
    Write-Host '  Check logs with:' -ForegroundColor Yellow
    Write-Host '  docker-compose logs n8n' -ForegroundColor Cyan
    exit 1
}
