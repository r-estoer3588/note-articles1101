#!/usr/bin/env pwsh
<#!
.SYNOPSIS
    Prompt Snapshot & Digest ランチャースクリプト
.DESCRIPTION
    Notionからスナップショットを取得し、LINE通知向けダイジェストを生成する
    Pythonツール（prompt_snapshot.py / prompt_digest.py）をPowerShellから快適に
    呼び出すための多機能ランチャーです。どのディレクトリからでも利用でき、
    依存チェック・セットアップ・エイリアス登録までまとめて行えます。
#>

[CmdletBinding()]
param(
    [switch]$Help,
    [switch]$Setup,
    [switch]$Snapshot,
    [switch]$Digest,
    [switch]$All,
    [string]$Mode = "daily",
    [int]$Limit = 5,
    [int]$StaleDays = 30,
    [string]$Output,
    [string]$JsonOutput,
    [switch]$Silent,
    [switch]$NoAliasPrompt
)

$ErrorActionPreference = "Stop"

# -------------------------------------------------------------
# 色付き出力ユーティリティ
# -------------------------------------------------------------
function Write-Header {
    param([string]$Message)
    Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
    Write-Host "🚀 $Message" -ForegroundColor Cyan
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Cyan
}

function Write-Info {
    param([string]$Message)
    Write-Host "🔍 $Message" -ForegroundColor Gray
}

function Write-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-WarningLine {
    param([string]$Message)
    Write-Host "⚠️  $Message" -ForegroundColor Yellow
}

function Write-ErrorLine {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

# -------------------------------------------------------------
# パス計算
# -------------------------------------------------------------
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
$SnapshotScript = Join-Path $RepoRoot "tools" | Join-Path -ChildPath "prompt_snapshot.py"
$DigestScript = Join-Path $RepoRoot "tools" | Join-Path -ChildPath "prompt_digest.py"
$SnapshotsDir = Join-Path $RepoRoot "data\prompt_snapshots"
$RequirementsFile = Join-Path $RepoRoot "requirements.txt"

# -------------------------------------------------------------
# ヘルプ
# -------------------------------------------------------------
function Show-LauncherHelp {
    Write-Header "Prompt Automation Launcher"
    Write-Host @"
使い方:
  .\tools\prompt_automation.ps1 [オプション]

主なオプション:
  -Setup             : 依存関係インストールとエイリアス登録
  -Snapshot          : prompt_snapshot.py を実行
  -Digest            : prompt_digest.py を実行
  -All               : Snapshot → Digest を連続実行（デフォルト動作）
  -Mode <daily|weekly|custom> : Digestモードを指定（既定: daily）
  -Limit <int>       : ダイジェスト各セクションの最大件数（既定: 5）
  -StaleDays <int>   : 利用推奨と判定する経過日数（既定: 30）
  -Output <path>     : ダイジェスト文字列の出力先ファイル
  -JsonOutput <path> : 統計情報のJSON出力先
  -Silent            : Pythonツールのサマリー表示を抑止
  -NoAliasPrompt     : Setup時にプロファイル追加案内をスキップ

例:
  # 初回セットアップ（依存インストール＋エイリアス登録）
  .\tools\prompt_automation.ps1 -Setup

  # スナップショットのみ実行
  .\tools\prompt_automation.ps1 -Snapshot

  # スナップショット → ダイジェスト（既定）
  .\tools\prompt_automation.ps1

  # ダイジェストをテキスト/JSONで保存
  .\tools\prompt_automation.ps1 -Digest -Output digest.txt -JsonOutput digest.json
"@
}

if ($Help) {
    Show-LauncherHelp
    return
}

# -------------------------------------------------------------
# 依存チェック
# -------------------------------------------------------------
function Test-Python {
    return [bool](Get-Command python -ErrorAction SilentlyContinue)
}

function Ensure-Python {
    if (-not (Test-Python)) {
        Write-ErrorLine "Python が見つかりません。"
        Write-Host "   👉 Microsoft Store または https://www.python.org/ から 3.11+ をインストールしてください" -ForegroundColor Yellow
        throw "PythonMissing"
    }
}

function Test-PipPackage {
    param([string]$Package)
    try {
        $null = python -m pip show $Package 2>$null
        return $LASTEXITCODE -eq 0
    } catch {
        return $false
    }
}

function Install-Dependencies {
    Ensure-Python
    if (-not (Test-Path $RequirementsFile)) {
        throw "requirements.txt が見つかりません ($RequirementsFile)"
    }
    Write-Info "pip 依存関係をインストール中..."
    python -m pip install -r $RequirementsFile | Write-Host
    if ($LASTEXITCODE -ne 0) {
        throw "pip install に失敗しました"
    }
    Write-Success "依存関係のインストール完了"
}

function Check-EnvVariables {
    $missing = @()
    if (-not $env:NOTION_API_KEY) { $missing += "NOTION_API_KEY" }
    if (-not $env:NOTION_DATABASE_ID) { $missing += "NOTION_DATABASE_ID" }
    if ($missing.Count -gt 0) {
        Write-WarningLine "Notion API の環境変数 (${missing -join ', '}) が未設定です。"
        Write-Host "   PowerShellでは以下のように設定できます:" -ForegroundColor Gray
        foreach ($key in $missing) {
            Write-Host "   setx $key 'your_value_here'" -ForegroundColor Yellow
        }
        Write-Host "   反映後は新しいターミナルを開いてください。" -ForegroundColor Gray
    } else {
        Write-Success "Notion API 環境変数を確認しました"
    }
}

# -------------------------------------------------------------
# プロファイル登録
# -------------------------------------------------------------
function Register-PromptAutomationAlias {
    param([string[]]$Aliases = @('pa','prompt'))

    $launcherPath = Join-Path $RepoRoot "tools\\prompt_automation.ps1"
    $profilePath = $PROFILE

    if (-not (Test-Path $profilePath)) {
        Write-Info "PowerShell プロファイルが未作成のため、新規作成します ($profilePath)"
        New-Item -ItemType File -Path $profilePath -Force | Out-Null
    }

    $profileContent = Get-Content $profilePath -Raw -ErrorAction SilentlyContinue
    $functionName = "Invoke-PromptAutomation"

    if ($profileContent -and $profileContent -match $functionName) {
        Write-WarningLine "既に $functionName が登録されています。必要に応じて手動で確認してください。"
        return
    }

    $aliasesBlock = ($Aliases | ForEach-Object { "Set-Alias $_ $functionName" }) -join "`n"

    $snippet = @"
function $functionName {
    param([Parameter(ValueFromRemainingArguments = $true)] [string[]]`$Args)
    & '$launcherPath' @Args
}
$aliasesBlock
"@

    Add-Content -Path $profilePath -Value "`n# Prompt Automation Launcher`n$snippet" -Encoding UTF8
    Write-Success "PowerShell プロファイルにエイリアス ($($Aliases -join ', ')) を登録しました"
    Write-Host "   次回のターミナルから 'pa' / 'prompt' コマンドで起動できます" -ForegroundColor Gray
}

# -------------------------------------------------------------
# Python実行ラッパー
# -------------------------------------------------------------
function Invoke-PythonScript {
    param(
        [Parameter(Mandatory)] [string]$ScriptPath,
        [string[]]$Arguments = @()
    )

    if (-not (Test-Path $ScriptPath)) {
        throw "スクリプトが見つかりません: $ScriptPath"
    }

    Ensure-Python

    Push-Location $RepoRoot
    try {
        Write-Info "python $([System.IO.Path]::GetFileName($ScriptPath)) $($Arguments -join ' ')"
        & python $ScriptPath @Arguments
        $exit = $LASTEXITCODE
    } finally {
        Pop-Location
    }

    if ($exit -ne 0) {
        throw "Pythonスクリプトがエラー終了しました (exit=$exit)"
    }
}

# -------------------------------------------------------------
# セットアップ処理
# -------------------------------------------------------------
function Invoke-LauncherSetup {
    Write-Header "Prompt Automation Setup"
    Install-Dependencies
    Check-EnvVariables

    if (-not $NoAliasPrompt) {
        $response = Read-Host "PowerShell プロファイルへエイリアス (pa/prompt) を登録しますか？ (y/N)"
        if ($response -match '^[Yy]') {
            Register-PromptAutomationAlias
        } else {
            Write-Info "エイリアス登録はスキップされました。必要になったら -Setup を再実行してください。"
        }
    }

    Write-Success "セットアップが完了しました"
}

# -------------------------------------------------------------
# スナップショット実行
# -------------------------------------------------------------
function Invoke-Snapshot {
    Write-Header "Prompt Snapshot"
    $args = @("--format","json","--output-dir",$SnapshotsDir)
    if ($Silent) { $args += "--silent" }
    Invoke-PythonScript -ScriptPath $SnapshotScript -Arguments $args
    Write-Success "スナップショットを $SnapshotsDir に保存しました"
}

# -------------------------------------------------------------
# ダイジェスト実行
# -------------------------------------------------------------
function Invoke-Digest {
    Write-Header "Prompt Digest"
    $args = @(
        "--snapshot-dir", $SnapshotsDir,
        "--mode", $Mode,
        "--limit", $Limit,
        "--stale-days", $StaleDays
    )
    if ($Output) { $args += @("--output", $Output) }
    if ($JsonOutput) { $args += @("--json-output", $JsonOutput) }
    if ($Silent) { $args += "--quiet" }
    Invoke-PythonScript -ScriptPath $DigestScript -Arguments $args
    Write-Success "ダイジェストの生成が完了しました"
    if ($Output) {
        Write-Host "   📄 Text: $Output" -ForegroundColor Gray
    }
    if ($JsonOutput) {
        Write-Host "   📊 JSON: $JsonOutput" -ForegroundColor Gray
    }
}

# -------------------------------------------------------------
# メイン処理
# -------------------------------------------------------------
try {
    if ($Setup) {
        Invoke-LauncherSetup
        if (-not ($Snapshot -or $Digest -or $All)) {
            return
        }
    }

    if ($All) {
        $Snapshot = $true
        $Digest = $true
    }

    if (-not $Snapshot -and -not $Digest) {
        # デフォルトは両方実行
        $Snapshot = $true
        $Digest = $true
    }

    if ($Snapshot -and -not (Test-PipPackage -Package "notion-client")) {
        Write-WarningLine "notion-client が見つかりません。-Setup でインストールしてください。"
    }

    if ($Snapshot) {
        Invoke-Snapshot
    }

    if ($Digest) {
        Invoke-Digest
    }

    Write-Success "すべての処理が完了しました"
} catch {
    Write-ErrorLine $_
    Write-Host "   💡 次のステップ: -Setup を実行して依存関係を整備 / 環境変数を設定してください" -ForegroundColor Yellow
    exit 1
}
