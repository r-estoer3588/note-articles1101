#Requires -Version 7.0
<#
.SYNOPSIS
    Learning - 自動学習ループツールランチャー

.DESCRIPTION
    X/note/Threadsの指標を収集し、AIに改善指示を出して過去の成功例で再教育する自動学習ツール。
    どのディレクトリからでも実行可能で、PowerShellプロファイルへの自動追加もサポート。

.PARAMETER Help
    ヘルプを表示

.PARAMETER Setup
    初回セットアップを実行（依存パッケージのインストール）

.PARAMETER Ingest
    X/note/Threads指標を収集してスナップショット保存

.PARAMETER Review
    前回投稿のKPI分析と改善提案を表示

.PARAMETER Replay
    過去の成功例を参照して再生成

.PARAMETER Goal
    目的を指定（例: "noteリード10件"）

.PARAMETER Deliverable
    成果物を指定（例: "2600文字記事"）

.EXAMPLE
    .\learning.ps1
    対話モードで起動

.EXAMPLE
    .\learning.ps1 -Ingest
    X/note/Threads指標を収集

.EXAMPLE
    .\learning.ps1 -Review
    前回のKPI分析

.EXAMPLE
    .\learning.ps1 -Replay
    成功例を元に再生成

.EXAMPLE
    learning
    どこからでも起動（プロファイル設定後）
#>

param(
    [switch]$Help,
    [switch]$Setup,
    [switch]$Ingest,
    [switch]$Review,
    [switch]$Replay,
    [string]$Goal,
    [string]$Deliverable
)

$ErrorActionPreference = "Stop"

# カラー出力関数
function Write-Header {
    param([string]$Message)
    Write-Host "`n$Message" -ForegroundColor Cyan
    Write-Host ("=" * $Message.Length) -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-Warning-Custom {
    param([string]$Message)
    Write-Host "⚠️  $Message" -ForegroundColor Yellow
}

function Write-Info {
    param([string]$Message)
    Write-Host "💡 $Message" -ForegroundColor Blue
}

function Write-Error-Custom {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

# スクリプトのディレクトリを取得
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# ヘルプ表示
if ($Help) {
    Write-Header "📋 Learning - 自動学習ループツール"
    Write-Host ""
    Write-Host "📝 これは何？"
    Write-Host "  X/note/Threadsの投稿成果を収集し、数値で検証して"
    Write-Host "  AIに改善指示を出し、過去の成功例で再教育する自動学習ツール。"
    Write-Host ""
    Write-Host "🎯 4つのステップ"
    Write-Host "  1️⃣  X/note/Threads指標収集（-Ingest）"
    Write-Host "  2️⃣  目的と成果物の明確化（-Goal/-Deliverable）"
    Write-Host "  3️⃣  数値検証とAI改善指示（-Review）"
    Write-Host "  4️⃣  過去の成功例で再教育（-Replay）"
    Write-Host ""
    Write-Host "🚀 基本的な使い方"
    Write-Host "  learning              # 対話モード（全ステップ実行）"
    Write-Host "  learning -Ingest      # 指標収集のみ"
    Write-Host "  learning -Review      # KPI分析のみ"
    Write-Host "  learning -Replay      # 成功例参照"
    Write-Host ""
    Write-Host "🎛️  オプション付き実行"
    Write-Host '  learning -Goal "noteリード10件" -Deliverable "2600文字記事"'
    Write-Host ""
    Write-Host "🔧 セットアップ"
    Write-Host "  learning -Setup       # 依存パッケージをインストール"
    Write-Host ""
    Write-Host "📂 データ保存先"
    Write-Host "  learning/snapshots/   # X/note/Threads指標スナップショット"
    Write-Host "  learning/prompts/     # AI改善指示プロンプト"
    Write-Host "  learning/feedback/    # 実績値＋気づきメモ"
    Write-Host ""
    Write-Host "💡 PowerShellプロファイルに追加するには："
    Write-Host "  function Start-LearningTool {" -ForegroundColor Gray
    Write-Host "      Push-Location $scriptDir" -ForegroundColor Gray
    Write-Host "      try { .\learning.ps1 @args }" -ForegroundColor Gray
    Write-Host "      finally { Pop-Location }" -ForegroundColor Gray
    Write-Host "  }" -ForegroundColor Gray
    Write-Host "  Set-Alias learning Start-LearningTool" -ForegroundColor Gray
    Write-Host "  Set-Alias le Start-LearningTool" -ForegroundColor Gray
    Write-Host ""
    exit 0
}

# セットアップ処理
if ($Setup) {
    Write-Header "🔧 Learning セットアップ"
    Write-Host ""
    
    # Python確認
    Write-Host "🔍 Python確認中..." -ForegroundColor Gray
    $pythonCmd = Get-Command python -ErrorAction SilentlyContinue
    if (-not $pythonCmd) {
        Write-Error-Custom "Pythonが見つかりません"
        Write-Host "   https://www.python.org/downloads/ からインストールしてください"
        exit 1
    }
    Write-Success "Python検出: $(python --version)"
    
    # 依存パッケージインストール
    Write-Host ""
    Write-Host "📦 依存パッケージをインストール中..." -ForegroundColor Gray
    Write-Host "   pandas, matplotlib, requests, pyperclip"
    
    try {
        pip install pandas matplotlib requests pyperclip 2>&1 | Out-Null
        Write-Success "依存パッケージのインストール完了"
    } catch {
        Write-Error-Custom "インストール失敗"
        Write-Host "   手動で実行: pip install pandas matplotlib requests pyperclip"
        exit 1
    }
    
    # ディレクトリ作成
    Write-Host ""
    Write-Host "📁 ディレクトリ構造作成中..." -ForegroundColor Gray
    $learningDir = Join-Path $scriptDir "learning"
    $dirs = @(
        (Join-Path $learningDir "snapshots"),
        (Join-Path $learningDir "prompts"),
        (Join-Path $learningDir "feedback")
    )
    foreach ($dir in $dirs) {
        if (-not (Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
            Write-Success "作成: $dir"
        }
    }
    
    Write-Host ""
    Write-Success "セットアップ完了！"
    Write-Info "次のコマンドで起動できます: learning"
    exit 0
}

# 環境チェック
Write-Host "🔍 環境チェック中..." -ForegroundColor Gray

# Python確認
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Error-Custom "Pythonが見つかりません"
    Write-Host "   インストール: https://www.python.org/downloads/"
    Write-Host ""
    Write-Host "   または以下を実行:"
    Write-Host "   .\learning.ps1 -Setup" -ForegroundColor Cyan
    exit 1
}

# Pythonスクリプト確認
$pythonScript = Join-Path $scriptDir "tools\learning_manager.py"
if (-not (Test-Path $pythonScript)) {
    Write-Error-Custom "learning_manager.py が見つかりません"
    Write-Host "   予期されるパス: $pythonScript"
    exit 1
}

# 依存パッケージ確認
Write-Host "📦 依存パッケージ確認中..." -ForegroundColor Gray
$requiredPackages = @("pandas", "matplotlib", "requests", "pyperclip")
$missingPackages = @()

foreach ($pkg in $requiredPackages) {
    $checkCmd = "python -c `"import $pkg`" 2>&1"
    $result = Invoke-Expression $checkCmd
    if ($LASTEXITCODE -ne 0) {
        $missingPackages += $pkg
    }
}

if ($missingPackages.Count -gt 0) {
    Write-Warning-Custom "不足しているパッケージ: $($missingPackages -join ', ')"
    Write-Host ""
    Write-Host "   以下を実行してセットアップ:"
    Write-Host "   .\learning.ps1 -Setup" -ForegroundColor Cyan
    exit 1
}

Write-Success "環境チェック完了"

# メイン実行
Write-Host ""
$currentDir = Get-Location
try {
    Set-Location $scriptDir
    
    # 引数構築
    $args = @()
    if ($Ingest) { $args += "--ingest" }
    if ($Review) { $args += "--review" }
    if ($Replay) { $args += "--replay" }
    if ($Goal) { $args += "--goal"; $args += "`"$Goal`"" }
    if ($Deliverable) { $args += "--deliverable"; $args += "`"$Deliverable`"" }
    
    # Pythonスクリプト実行
    if ($args.Count -gt 0) {
        $cmd = "python `"$pythonScript`" $($args -join ' ')"
        Invoke-Expression $cmd
    } else {
        # 対話モード
        python "$pythonScript"
    }
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "   詳細: learning -Help" -ForegroundColor Gray
    }
} finally {
    Set-Location $currentDir
}
