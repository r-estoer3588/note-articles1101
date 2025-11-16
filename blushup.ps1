#!/usr/bin/env pwsh
<#
.SYNOPSIS
    BlushUp - プロンプト品質向上ツールランチャー

.DESCRIPTION
    GitHub Copilot Chatで使う品質向上プロンプトを辞書管理し、
    選択したプロンプトを@workspace付きでクリップボードにコピーします。

.PARAMETER Help
    ヘルプを表示します

.PARAMETER List
    利用可能なプロンプト一覧を表示します

.PARAMETER Show
    指定されたプロンプトを表示してクリップボードにコピーします

.PARAMETER Setup
    初回セットアップを実行します（依存パッケージのインストール）

.EXAMPLE
    .\blushup.ps1
    対話モードで起動

.EXAMPLE
    .\blushup.ps1 -List
    プロンプト一覧を表示

.EXAMPLE
    .\blushup.ps1 -Show 1
    プロンプト1（品質担保）をクリップボードにコピー

.EXAMPLE
    blushup
    どこからでも実行（PowerShellプロファイル設定後）

.EXAMPLE
    bu -Show 5
    短縮エイリアスで全部盛りプロンプトをコピー
#>

param(
    [switch]$Help,
    [switch]$List,
    [string]$Show,
    [switch]$Setup
)

$ErrorActionPreference = "Stop"

# カラー出力関数
function Write-Header {
    param([string]$Message)
    Write-Host ""
    Write-Host ("=" * 60) -ForegroundColor Cyan
    Write-Host $Message -ForegroundColor Cyan
    Write-Host ("=" * 60) -ForegroundColor Cyan
    Write-Host ""
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
    Write-Host "💡 $Message" -ForegroundColor Cyan
}

function Write-Error-Custom {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

# ヘルプ表示
if ($Help) {
    Write-Header "📋 BlushUp - プロンプト品質向上ツール"
    
    Write-Host "GitHub Copilot Chatで使う品質向上プロンプトを辞書管理し、" -ForegroundColor White
    Write-Host "選択したプロンプトを@workspace付きでクリップボードにコピーします。" -ForegroundColor White
    Write-Host ""
    
    Write-Host "【利用可能なプロンプト】" -ForegroundColor Yellow
    Write-Host "  1. 品質担保        - 細かいことでも全て質問"
    Write-Host "  2. 前提確認        - 解釈を箇条書きで確認"
    Write-Host "  3. チェックリスト  - 見落とし指摘"
    Write-Host "  4. 自己評価        - 尋ねるべきだった質問"
    Write-Host "  5. 全部盛り        - 1+2+3の組み合わせ"
    Write-Host ""
    
    Write-Host "【使い方】" -ForegroundColor Yellow
    Write-Host "  blushup              # 対話モードで起動"
    Write-Host "  blushup -List        # プロンプト一覧表示"
    Write-Host "  blushup -Show 1      # プロンプト1をコピー"
    Write-Host "  blushup -Show 5      # 全部盛りをコピー"
    Write-Host "  bu -Show 2           # 短縮エイリアス"
    Write-Host ""
    
    Write-Host "【初回セットアップ】" -ForegroundColor Yellow
    Write-Host "  blushup -Setup       # 依存パッケージをインストール"
    Write-Host ""
    
    Write-Host "【PowerShellプロファイル設定】" -ForegroundColor Yellow
    Write-Host "  以下をPowerShellプロファイルに追加すると、どこからでも実行可能になります："
    Write-Host ""
    Write-Host "  function Start-BlushUpTool {" -ForegroundColor Gray
    Write-Host "      Push-Location `"$PSScriptRoot`"" -ForegroundColor Gray
    Write-Host "      try { .\blushup.ps1 @args }" -ForegroundColor Gray
    Write-Host "      finally { Pop-Location }" -ForegroundColor Gray
    Write-Host "  }" -ForegroundColor Gray
    Write-Host "  Set-Alias blushup Start-BlushUpTool" -ForegroundColor Gray
    Write-Host "  Set-Alias bu Start-BlushUpTool" -ForegroundColor Gray
    Write-Host ""
    
    exit 0
}

# セットアップ
if ($Setup) {
    Write-Header "🔧 BlushUp セットアップ"
    
    Write-Host "依存パッケージをインストールします..." -ForegroundColor White
    Write-Host ""
    
    # pyperclip インストール
    Write-Host "📦 pyperclip をインストール中..." -ForegroundColor Cyan
    try {
        python -m pip install pyperclip --quiet
        Write-Success "pyperclip のインストールが完了しました"
    } catch {
        Write-Error-Custom "pyperclip のインストールに失敗しました"
        Write-Host "   手動でインストールしてください: pip install pyperclip" -ForegroundColor Yellow
    }
    
    Write-Host ""
    Write-Success "セットアップが完了しました！"
    Write-Host ""
    Write-Info "次のコマンドで起動できます: blushup"
    Write-Host ""
    
    exit 0
}

# Python存在チェック
try {
    $null = python --version 2>&1
} catch {
    Write-Error-Custom "Python が見つかりません"
    Write-Host ""
    Write-Host "   Python 3.8以降をインストールしてください" -ForegroundColor Yellow
    Write-Host "   https://www.python.org/downloads/" -ForegroundColor Cyan
    Write-Host ""
    exit 1
}

# pyperclip チェック
$pyperclipCheck = python -c "import pyperclip" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Warning-Custom "pyperclip がインストールされていません"
    Write-Host ""
    Write-Host "   クリップボード機能を使うには、以下を実行してください：" -ForegroundColor Yellow
    Write-Host "   blushup -Setup" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "   または手動でインストール：" -ForegroundColor Yellow
    Write-Host "   pip install pyperclip" -ForegroundColor Cyan
    Write-Host ""
    
    $continue = Read-Host "このまま続けますか？ (プロンプトの表示のみ可能) (y/n)"
    if ($continue -ne "y") {
        exit 1
    }
}

# プロジェクトルートに移動
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $scriptDir

try {
    # Python スクリプト実行
    $pythonScript = Join-Path $scriptDir "tools\blushup_prompt_manager.py"
    
    if (-not (Test-Path $pythonScript)) {
        Write-Error-Custom "スクリプトが見つかりません: $pythonScript"
        exit 1
    }
    
    # 引数を構築
    $pythonArgs = @()
    if ($List) {
        $pythonArgs += "--list"
    } elseif ($Show) {
        $pythonArgs += "--show", $Show
    }
    
    # Python実行
    if ($pythonArgs.Count -gt 0) {
        python $pythonScript @pythonArgs
    } else {
        python $pythonScript
    }
    
    $exitCode = $LASTEXITCODE
    
    if ($exitCode -eq 0) {
        Write-Host ""
        Write-Info "次回も使いやすいように、PowerShellプロファイルに設定することをおすすめします"
        Write-Host "   詳細: blushup -Help" -ForegroundColor Gray
        Write-Host ""
    }
    
    exit $exitCode
    
} finally {
    Pop-Location
}
