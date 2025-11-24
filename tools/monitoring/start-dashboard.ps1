# Buffer Monitoring Dashboard Launcher
# PowerShellプロファイルから呼び出し可能

function Start-BufferDashboard {
    [CmdletBinding()]
    param(
        [Parameter()]
        [string]$Path = "c:\Repos\note-articles\tools\monitoring"
    )

    Write-Host "🚀 Starting Buffer Monitoring Dashboard..." -ForegroundColor Cyan
    Write-Host ""

    # Check if path exists
    if (-not (Test-Path $Path)) {
        Write-Host "❌ Error: Monitoring directory not found at $Path" -ForegroundColor Red
        Write-Host "Please update the path in your PowerShell profile." -ForegroundColor Yellow
        return
    }

    # Change directory
    Push-Location $Path

    try {
        # Start server in background
        Write-Host "📡 Starting server on port 8000..." -ForegroundColor Green
        $job = Start-Job -ScriptBlock {
            param($dir)
            Set-Location $dir
            python server.py
        } -ArgumentList $Path

        # Wait a moment for server to start
        Start-Sleep -Seconds 2

        # Open browser
        Write-Host "🌐 Opening dashboard in browser..." -ForegroundColor Green
        Start-Process "http://localhost:8000/dashboard.html"

        Write-Host ""
        Write-Host "✅ Dashboard is running!" -ForegroundColor Green
        Write-Host ""
        Write-Host "ℹ️  Server Job ID: $($job.Id)" -ForegroundColor Cyan
        Write-Host "ℹ️  To stop the server, run: Stop-Job -Id $($job.Id); Remove-Job -Id $($job.Id)" -ForegroundColor Cyan
        Write-Host ""

        # Store job ID globally for easy access
        $Global:BufferDashboardJob = $job

        Write-Host "💡 Quick stop command: Stop-BufferDashboard" -ForegroundColor Yellow
    }
    catch {
        Write-Host "❌ Error starting dashboard: $_" -ForegroundColor Red
    }
    finally {
        Pop-Location
    }
}

function Stop-BufferDashboard {
    [CmdletBinding()]
    param()

    if ($Global:BufferDashboardJob) {
        Write-Host "🛑 Stopping Buffer Dashboard server..." -ForegroundColor Yellow
        Stop-Job -Id $Global:BufferDashboardJob.Id
        Remove-Job -Id $Global:BufferDashboardJob.Id
        $Global:BufferDashboardJob = $null
        Write-Host "✅ Server stopped." -ForegroundColor Green
    }
    else {
        Write-Host "ℹ️  No active dashboard server found." -ForegroundColor Cyan
    }
}

# Alias for convenience
Set-Alias -Name dashboard -Value Start-BufferDashboard

# Export functions
Export-ModuleMember -Function Start-BufferDashboard, Stop-BufferDashboard -Alias dashboard
