param(
    [Parameter(Mandatory=$true)]
    [string]$RepoUrl,
    [string]$Branch = "main"
)

Write-Host "[init_and_push] Initializing git repo in $(Get-Location)" -ForegroundColor Cyan

if (-not (Test-Path ".git")) {
    git init | Out-Null
}

# Basic config (optional, comment out if you already have global config)
# git config user.name "<your-name>"
# git config user.email "<your-email>"

# Create first commit if none exists
$hasCommit = $null -ne (git rev-parse --verify HEAD 2>$null)
if (-not $hasCommit) {
    git add .
    git commit -m "init: import note-articles structure with first article" | Out-Null
}

# Set remote (idempotent)
$existingRemote = git remote get-url origin 2>$null
if (-not $existingRemote) {
    git remote add origin $RepoUrl
} else {
    Write-Host "[init_and_push] Remote 'origin' already set to: $existingRemote" -ForegroundColor Yellow
}

# Push
git branch -M $Branch
 git push -u origin $Branch

Write-Host "[init_and_push] Done. Repo pushed to $RepoUrl ($Branch)" -ForegroundColor Green
