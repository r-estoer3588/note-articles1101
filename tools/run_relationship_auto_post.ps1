# Run Relationship Auto Poster
# This script is intended to be run by Task Scheduler every hour (or 30 mins)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
$VenvPath = Join-Path $RepoRoot ".venv"

# Activate Venv
if (Test-Path "$VenvPath\Scripts\Activate.ps1") {
    & "$VenvPath\Scripts\Activate.ps1"
} else {
    Write-Host "Virtual environment not found at $VenvPath"
    exit 1
}

# Run the auto poster
# Use --check to just run the check logic
python "$ScriptDir\relationship_auto_poster.py" --check

# If you need to reset the start date, uncomment and run once:
# python "$ScriptDir\relationship_auto_poster.py" --reset-start-date "2025-11-22"
