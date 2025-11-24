# PowerShell プロファイル用設定
# このファイルの内容を PowerShell プロファイルに追加してください

# 教育カテゴリ別投稿生成ツールのエイリアス
function Start-EducationTool {
    Push-Location C:\Repos\note-articles
    try {
        .\education.ps1 @args
    }
    finally {
        Pop-Location
    }
}

# 品質向上ツールのエイリアス
function Start-BlushUpTool {
    Push-Location C:\Repos\note-articles
    try {
        .\blushup.ps1 @args
    }
    finally {
        Pop-Location
    }
}

# げすいぬ化記事改善ツールのエイリアス
function Start-GesuinuTool {
    Push-Location C:\Repos\note-articles
    try {
        .\gesuinu.ps1 @args
    }
    finally {
        Pop-Location
    }
}

# マネタイズプラン生成ツールのエイリアス
function Start-MonetizeTool {
    Push-Location C:\Repos\note-articles
    try {
        .\monetize.ps1 @args
    }
    finally {
        Pop-Location
    }
}

# 錬金王スタイル記事リライトツールのエイリアス
function Start-RenkinTool {
    Push-Location C:\Repos\note-articles
    try {
        .\renkin.ps1 @args
    }
    finally {
        Pop-Location
    }
}

# SNS統合分析ツールのエイリアス
function Update-SnsStats {
    Push-Location C:\Repos\note-articles
    try {
        python tools/sns_integrated_analyzer.py @args
    }
    finally {
        Pop-Location
    }
}

# Buffer モニタリングダッシュボード
function Start-BufferDashboard {
    [CmdletBinding()]
    param(
        [Parameter()]
        [string]$Path = "C:\Repos\note-articles\tools\monitoring"
    )

    Write-Host "🚀 Starting Buffer Monitoring Dashboard..." -ForegroundColor Cyan

    if (-not (Test-Path $Path)) {
        Write-Host "❌ Error: Monitoring directory not found at $Path" -ForegroundColor Red
        return
    }

    Push-Location $Path

    try {
        # Start server in background
        $job = Start-Job -ScriptBlock {
            param($dir)
            Set-Location $dir
            python server.py
        } -ArgumentList $Path

        # Wait for server to start
        Start-Sleep -Seconds 2

        # Open browser
        Start-Process "http://localhost:8000/dashboard.html"

        Write-Host "✅ Dashboard is running! (Job ID: $($job.Id))" -ForegroundColor Green
        Write-Host "💡 To stop: Stop-BufferDashboard" -ForegroundColor Yellow

        # Store job ID globally
        $Global:BufferDashboardJob = $job
    }
    catch {
        Write-Host "❌ Error: $_" -ForegroundColor Red
    }
    finally {
        Pop-Location
    }
}

function Stop-BufferDashboard {
    if ($Global:BufferDashboardJob) {
        Write-Host "🛑 Stopping dashboard server..." -ForegroundColor Yellow
        Stop-Job -Id $Global:BufferDashboardJob.Id
        Remove-Job -Id $Global:BufferDashboardJob.Id
        $Global:BufferDashboardJob = $null
        Write-Host "✅ Server stopped." -ForegroundColor Green
    }
    else {
        Write-Host "ℹ️  No active dashboard server found." -ForegroundColor Cyan
    }
}

# Threads成長記録ツールのエイリアス
function Start-ThreadsReport {
    Push-Location C:\Repos\note-articles
    try {
        python tools/daily_report.py @args
    }
    finally {
        Pop-Location
    }
}

# エイリアス設定
Set-Alias education Start-EducationTool
Set-Alias edu Start-EducationTool
Set-Alias blushup Start-BlushUpTool
Set-Alias bu Start-BlushUpTool
Set-Alias gesuinu Start-GesuinuTool
Set-Alias gn Start-GesuinuTool
Set-Alias monetize Start-MonetizeTool
Set-Alias mz Start-MonetizeTool
Set-Alias renkin Start-RenkinTool
Set-Alias rk Start-RenkinTool
Set-Alias sns Update-SnsStats
Set-Alias dashboard Start-BufferDashboard
Set-Alias db Start-BufferDashboard
Set-Alias report-threads Start-ThreadsReport
Set-Alias rt Start-ThreadsReport

# バナー表示
Write-Host "PowerShell $($PSVersionTable.PSVersion)" -ForegroundColor Cyan
Write-Host "📝 教育ツール: education または edu" -ForegroundColor Green
Write-Host "🎯 品質向上: blushup または bu" -ForegroundColor Yellow
Write-Host "🐕 げすいぬ化: gesuinu または gn" -ForegroundColor Red
Write-Host "💰 マネタイズ: monetize または mz" -ForegroundColor DarkYellow
Write-Host "🔱 錬金王note: renkin または rk" -ForegroundColor Magenta
Write-Host "📊 SNS分析: sns" -ForegroundColor Cyan
Write-Host "📈 Bufferダッシュボード: dashboard または db" -ForegroundColor Blue
Write-Host "🧵 Threads報告: report-threads または rt" -ForegroundColor White

# 使い方:
# どのディレクトリからでも以下のコマンドで起動:
#   education / edu      # 教育カテゴリ別投稿生成
#   blushup / bu         # プロンプト品質向上
#   gesuinu / gn         # げすいぬ化記事改善
#   monetize / mz        # マネタイズプラン生成
#   renkin / rk          # 錬金王スタイル記事リライト
#   sns                  # SNS統合分析

