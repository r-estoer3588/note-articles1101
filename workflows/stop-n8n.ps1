# n8n Notes Organizer - Stop Script
# Settings are preserved, only stops the container

Write-Host 'Stopping n8n Notes Organizer...' -ForegroundColor Yellow

# Move to script directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# Check if docker-compose.yml exists
if (-not (Test-Path 'docker-compose.yml')) {
    Write-Host 'ERROR: docker-compose.yml not found' -ForegroundColor Red
    Write-Host '  Please run this script in the workflows/ directory' -ForegroundColor Yellow
    exit 1
}

# Confirm whether to keep settings
Write-Host ''
Write-Host 'WARNING: Stop with settings preserved? (Recommended)' -ForegroundColor Yellow
Write-Host '  Y = Stop and keep settings (Recommended)' -ForegroundColor Green
Write-Host '  N = Stop and delete all settings' -ForegroundColor Red
Write-Host ''
Write-Host 'Choose (Y/n): ' -NoNewline -ForegroundColor White
$response = Read-Host

if ($response -eq 'n' -or $response -eq 'N') {
    Write-Host ''
    Write-Host 'WARNING: Really delete all settings?' -ForegroundColor Red
    Write-Host '  This will delete workflows and API keys' -ForegroundColor Yellow
    Write-Host ''
    Write-Host 'Type DELETE to confirm: ' -NoNewline -ForegroundColor White
    $confirm = Read-Host
    
    if ($confirm -eq 'DELETE') {
        Write-Host ''
        Write-Host 'Deleting settings and stopping container...' -ForegroundColor Red
        docker-compose down -v
        Write-Host ''
        Write-Host 'All settings deleted' -ForegroundColor Yellow
        Write-Host '  First-time setup required on next start' -ForegroundColor Cyan
    } else {
        Write-Host ''
        Write-Host 'Cancelled (no changes made)' -ForegroundColor Green
        exit 0
    }
} else {
    # Stop while keeping settings
    Write-Host ''
    Write-Host 'Stopping container while keeping settings...' -ForegroundColor Cyan
    docker-compose down
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ''
        Write-Host 'n8n stopped successfully' -ForegroundColor Green
        Write-Host '  Settings are preserved' -ForegroundColor Cyan
        Write-Host ''
        Write-Host 'To restart:' -ForegroundColor White
        Write-Host '  .\start-n8n.ps1' -ForegroundColor Yellow
        Write-Host ''
        Write-Host '  or' -ForegroundColor White
        Write-Host '  docker-compose up -d' -ForegroundColor Yellow
    } else {
        Write-Host ''
        Write-Host 'ERROR: Failed to stop' -ForegroundColor Red
        exit 1
    }
}
