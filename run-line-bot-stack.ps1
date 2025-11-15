param(
    [switch]$NoTunnel
)

$ErrorActionPreference = 'Stop'

$venvPython = "C:/Repos/.venv/Scripts/python.exe"
$scriptPath = "C:/Repos/note-articles/tools/line_bot_api.py"
$ltPort = 5678
$ltSubdomain = "hogey-linebot"

Write-Host "[line-bot] Using venv python: $venvPython"

if (!(Test-Path $venvPython)) {
    Write-Error "venv python not found: $venvPython"
    exit 1
}

# ---- Flask state API ----
$flaskListening = netstat -ano | Select-String ":5679" -ErrorAction SilentlyContinue
if (-not $flaskListening) {
    Write-Host "[line-bot] Starting Flask state API on 5679..."
    Start-Process -FilePath $venvPython -ArgumentList $scriptPath -WindowStyle Hidden
} else {
    Write-Host "[line-bot] Flask already listening on 5679"
}

# ---- localtunnel ----
if (-not $NoTunnel) {
    $nodeProcs = Get-Process node -ErrorAction SilentlyContinue
    $ltRunning = $false
    if ($nodeProcs) {
        foreach ($p in $nodeProcs) {
            try {
                $cmdLine = (Get-CimInstance Win32_Process -Filter "ProcessId = $($p.Id)").CommandLine
                if ($cmdLine -and $cmdLine -like "*localtunnel*--port $ltPort*" ) {
                    $ltRunning = $true
                    break
                }
            } catch {
            }
        }
    }

    if (-not $ltRunning) {
        Write-Host "[line-bot] Starting localtunnel on port $ltPort (subdomain: $ltSubdomain)..."
        Start-Process -FilePath "npx" -ArgumentList "localtunnel --port $ltPort --subdomain $ltSubdomain" -WindowStyle Hidden
    } else {
        Write-Host "[line-bot] localtunnel already running"
    }
} else {
    Write-Host "[line-bot] Skipping localtunnel because -NoTunnel is set"
}
