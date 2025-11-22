#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Gesuinu - げすいぬ化記事改善ツールランチャー

.DESCRIPTION
    既存の記事をげすいぬスタイル（月収30万円層向け）に変換するツール。
    article_quality_evaluation_prompt_v3_gesuinu.txt に基づいて、
    4つの成功指標（Trust/Empathy/Values/Encouragement）すべて4.0以上を目指します。

.PARAMETER Help
    ヘルプを表示します

.PARAMETER File
    変換対象の記事ファイルパスを指定します

.PARAMETER Show
    げすいぬ化プロンプトを表示してクリップボードにコピーします

.PARAMETER Evaluate
    記事を4つの指標で評価します（改善案なし）

.PARAMETER Setup
    初回セットアップを実行します（依存パッケージのインストール）

.EXAMPLE
    .\gesuinu.ps1
    対話モードで起動

.EXAMPLE
    .\gesuinu.ps1 -File "articles/2025-11-16_sample/article.md"
    指定した記事をげすいぬ化

.EXAMPLE
    .\gesuinu.ps1 -Show
    げすいぬ化プロンプトをクリップボードにコピー

.EXAMPLE
    .\gesuinu.ps1 -Evaluate -File "articles/sample.md"
    記事を評価のみ実行

.EXAMPLE
    gesuinu -File "articles/sample.md"
    どこからでも実行（PowerShellプロファイル設定後）

.EXAMPLE
    gn -Show
    短縮エイリアスでプロンプトをコピー
#>

param(
    [switch]$Help,
    [string]$File,
    [switch]$Show,
    [switch]$Evaluate,
    [switch]$Setup
)

$ErrorActionPreference = "Stop"

# カラー出力関数
function Write-Header {
    param([string]$Message)
    Write-Host ""
    Write-Host ("=" * 70) -ForegroundColor Cyan
    Write-Host $Message -ForegroundColor Cyan
    Write-Host ("=" * 70) -ForegroundColor Cyan
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
    Write-Header "🐕 Gesuinu - げすいぬ化記事改善ツール"
    
    Write-Host "既存の記事をげすいぬスタイル（月収30万円層向け）に変換します。" -ForegroundColor White
    Write-Host "4つの成功指標すべてで4.0以上を目指します。" -ForegroundColor White
    Write-Host ""
    
    Write-Host "【4つの成功指標】" -ForegroundColor Yellow
    Write-Host "  1. 信頼構築 (Trust)       - データ出典、自分の損失額開示、計算根拠"
    Write-Host "  2. 共感構築 (Empathy)     - 失敗開示、「あなた」統一、業界への毒+根拠"
    Write-Host "  3. 価値観共有 (Values)    - 執筆理念、構造批判、読者利益優先"
    Write-Host "  4. 励まし (Encouragement) - 3ステップ、ハードル低減、背中押し"
    Write-Host ""
    
    Write-Host "【ターゲット読者像】" -ForegroundColor Yellow
    Write-Host "  • 年収: 400-500万円（月収30万円前後）"
    Write-Host "  • 年齢: 30代中心"
    Write-Host "  • 状態: 構造に気づき始めた、家族あり、将来不安、現実的思考"
    Write-Host "  • 心理: 「努力は報われる」への疑問、AI・自動化への期待"
    Write-Host ""
    
    Write-Host "【使い方】" -ForegroundColor Yellow
    Write-Host "  gesuinu                              # 対話モードで起動"
    Write-Host "  gesuinu -File 'articles/sample.md'   # 指定記事をげすいぬ化"
    Write-Host "  gesuinu -Show                        # プロンプトをコピー"
    Write-Host "  gesuinu -Evaluate -File 'sample.md'  # 評価のみ実行"
    Write-Host "  gn -Show                             # 短縮エイリアス"
    Write-Host ""
    
    Write-Host "【初回セットアップ】" -ForegroundColor Yellow
    Write-Host "  gesuinu -Setup       # 依存パッケージをインストール"
    Write-Host ""
    
    Write-Host "【PowerShellプロファイル設定】" -ForegroundColor Yellow
    Write-Host "  以下をPowerShellプロファイルに追加すると、どこからでも実行可能になります："
    Write-Host ""
    Write-Host "  function Start-GesuinuTool {" -ForegroundColor Gray
    Write-Host "      Push-Location `"$PSScriptRoot`"" -ForegroundColor Gray
    Write-Host "      try { .\gesuinu.ps1 @args }" -ForegroundColor Gray
    Write-Host "      finally { Pop-Location }" -ForegroundColor Gray
    Write-Host "  }" -ForegroundColor Gray
    Write-Host "  Set-Alias gesuinu Start-GesuinuTool" -ForegroundColor Gray
    Write-Host "  Set-Alias gn Start-GesuinuTool" -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "【関連ファイル】" -ForegroundColor Yellow
    Write-Host "  • プロンプト: prompt/article_quality_evaluation_prompt_v3_gesuinu.txt"
    Write-Host "  • GPT用: archive/prompt/gesuinu_gpt_persona_v2.txt (廃止済み)"
    Write-Host "  • 記事生成: gethnote/prompt/geth_prompt.txt"
    Write-Host ""
    
    exit 0
}

# セットアップ
if ($Setup) {
    Write-Header "🔧 Gesuinu セットアップ"
    
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
    Write-Info "次のコマンドで起動できます: gesuinu"
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
    Write-Host "   gesuinu -Setup" -ForegroundColor Cyan
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
    $pythonScript = Join-Path $scriptDir "tools\gesuinu_prompt_manager.py"
    
    if (-not (Test-Path $pythonScript)) {
        Write-Error-Custom "スクリプトが見つかりません: $pythonScript"
        exit 1
    }
    
    # 引数を構築
    $pythonArgs = @()
    if ($Show) {
        $pythonArgs += "--show"
    } elseif ($File) {
        $pythonArgs += "--file", $File
        if ($Evaluate) {
            $pythonArgs += "--evaluate"
        }
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
        Write-Host "   詳細: gesuinu -Help" -ForegroundColor Gray
        Write-Host ""
    }
    
    exit $exitCode
    
} finally {
    Pop-Location
}
