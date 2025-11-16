#!/usr/bin/env pwsh
# -*- coding: utf-8 -*-
<#
.SYNOPSIS
    教育カテゴリ別X投稿生成ツール - ワンコマンド起動

.DESCRIPTION
    6つの教育カテゴリ（信用/目的/問題/手段/投資/行動）から選んで、
    AIで自動的にX投稿案を3つ生成します。

.EXAMPLE
    .\education.ps1
    # 対話モードで投稿生成（推奨）

.EXAMPLE
    .\education.ps1 -Help
    # 使い方とセットアップ方法を表示

.EXAMPLE
    .\education.ps1 -Setup
    # 初回セットアップ（依存関係インストール + API設定ガイド）

.EXAMPLE
    .\education.ps1 -List
    # カテゴリ一覧表示
#>

param(
    [switch]$Help,
    [switch]$Setup,
    [switch]$List
)

$ErrorActionPreference = "Stop"
$PSDefaultParameterValues['*:Encoding'] = 'utf8'

# カラー出力
function Write-Header {
    param([string]$Text)
    Write-Host "`n$('=' * 60)" -ForegroundColor Cyan
    Write-Host "  $Text" -ForegroundColor Cyan
    Write-Host "$('=' * 60)`n" -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Text)
    Write-Host "✅ $Text" -ForegroundColor Green
}

function Write-Warning-Custom {
    param([string]$Text)
    Write-Host "⚠️  $Text" -ForegroundColor Yellow
}

function Write-Info {
    param([string]$Text)
    Write-Host "💡 $Text" -ForegroundColor Blue
}

# ヘルプ表示
if ($Help) {
    Write-Header "教育カテゴリ別投稿生成ツール"
    
    Write-Host "📝 これは何？"
    Write-Host "  X（旧Twitter）の投稿を心理学に基づいた6つのカテゴリで自動生成するツールです。"
    Write-Host ""
    Write-Host "🎯 6つの教育カテゴリ"
    Write-Host "  1. 信用   - 信頼・共感・安心感の構築"
    Write-Host "  2. 目的   - 理想未来の明確化と動機形成"
    Write-Host "  3. 問題   - 現状の限界と真因認識"
    Write-Host "  4. 手段   - 解決策の期待醸成"
    Write-Host "  5. 投資   - コストの正当化と価値提示"
    Write-Host "  6. 行動   - 即時アクション誘発"
    Write-Host ""
    Write-Host "🚀 基本的な使い方"
    Write-Host "  .\education.ps1"
    Write-Host "  ↓"
    Write-Host "  1. カテゴリ番号を入力（1〜6）"
    Write-Host "  2. ゴール入力（例: フォロワー獲得）"
    Write-Host "  3. ペルソナ入力（例: 30代会社員/副業中）"
    Write-Host "  4. 問題点入力（例: 時間がない）"
    Write-Host "  5. トーン入力（例: 共感的）"
    Write-Host "  6. テーマ入力（例: 1日15分でできる副業習慣）"
    Write-Host "  ↓"
    Write-Host "  ✨ AIが3つの投稿案を自動生成！"
    Write-Host ""
    Write-Host "🔧 コマンド一覧"
    Write-Host "  .\education.ps1          # 対話モードで投稿生成"
    Write-Host "  .\education.ps1 -Help    # このヘルプを表示"
    Write-Host "  .\education.ps1 -Setup   # 初回セットアップ"
    Write-Host "  .\education.ps1 -List    # カテゴリ一覧表示"
    Write-Host ""
    Write-Host "📄 詳細ドキュメント"
    Write-Host "  tools\README_education_prompt.md"
    Write-Host "  tools\.github-copilot-instructions.md"
    Write-Host ""
    exit 0
}

# セットアップ
if ($Setup) {
    Write-Header "初回セットアップ"
    
    Write-Host "📦 ステップ1: 必要なPythonパッケージをインストール"
    Write-Host ""
    
    $packages = @("openai", "pyperclip")
    foreach ($pkg in $packages) {
        Write-Host "  インストール中: $pkg" -ForegroundColor Gray
        pip install $pkg --quiet
    }
    Write-Success "パッケージインストール完了"
    Write-Host ""
    
    Write-Host "🔑 ステップ2: OpenAI APIキーの設定（任意）"
    Write-Host ""
    Write-Info "APIキーを設定すると、投稿が自動生成されます"
    Write-Info "未設定でもプロンプトだけ表示されるので使えます"
    Write-Host ""
    
    $apiKey = [System.Environment]::GetEnvironmentVariable("OPENAI_API_KEY", "User")
    
    if ($apiKey) {
        Write-Success "APIキーは既に設定済みです"
    } else {
        Write-Host "  1. APIキー取得: https://platform.openai.com/api-keys"
        Write-Host "  2. 以下のコマンドで設定（PowerShellを再起動後に有効）:"
        Write-Host ""
        Write-Host '  [System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "sk-proj-あなたのキー", "User")' -ForegroundColor Yellow
        Write-Host ""
        Write-Info "後で設定する場合: .\education.ps1 -Setup を再実行"
    }
    Write-Host ""
    
    Write-Header "セットアップ完了"
    Write-Host "✅ 準備ができました！以下のコマンドで実行:"
    Write-Host ""
    Write-Host "  .\education.ps1" -ForegroundColor Green
    Write-Host ""
    exit 0
}

# カテゴリ一覧
if ($List) {
    Write-Host ""
    python tools\education_prompt_manager.py --list
    Write-Host ""
    exit 0
}

# メイン実行
Write-Header "教育カテゴリ別投稿生成ツール"

# Python環境チェック
try {
    $null = python --version
} catch {
    Write-Host "❌ Pythonが見つかりません" -ForegroundColor Red
    Write-Host "   Python 3.8以上をインストールしてください"
    Write-Host "   https://www.python.org/downloads/"
    exit 1
}

# スクリプト存在チェック
$scriptPath = "tools\education_prompt_manager.py"
if (-not (Test-Path $scriptPath)) {
    Write-Host "❌ スクリプトが見つかりません: $scriptPath" -ForegroundColor Red
    Write-Host "   note-articlesディレクトリから実行してください"
    exit 1
}

# 依存関係チェック（簡易）
Write-Host "🔍 環境チェック中..." -ForegroundColor Gray
$hasOpenAI = python -c "import openai" 2>$null
$hasPyperclip = python -c "import pyperclip" 2>$null

if (-not $?) {
    Write-Host ""
    Write-Warning-Custom "必要なパッケージが不足しています"
    Write-Host ""
    Write-Host "  以下のコマンドでセットアップしてください:"
    Write-Host ""
    Write-Host "  .\education.ps1 -Setup" -ForegroundColor Yellow
    Write-Host ""
    $response = Read-Host "今すぐセットアップしますか？ (Y/n)"
    if ($response -eq "" -or $response -eq "Y" -or $response -eq "y") {
        & $PSCommandPath -Setup
        exit 0
    }
    Write-Host ""
}

# API設定確認
$apiKey = $env:OPENAI_API_KEY
if (-not $apiKey) {
    $apiKey = [System.Environment]::GetEnvironmentVariable("OPENAI_API_KEY", "User")
}

if (-not $apiKey) {
    Write-Host ""
    Write-Info "OpenAI APIキーが未設定です"
    Write-Info "GitHub Copilot Chat統合モードで実行します"
    Write-Host ""
    Write-Host "  💡 完成したプロンプトを " -NoNewline -ForegroundColor Cyan
    Write-Host "@workspace" -NoNewline -ForegroundColor Green
    Write-Host " に貼り付けて実行できます" -ForegroundColor Cyan
    Write-Host "     または OpenAI API設定: " -NoNewline -ForegroundColor DarkGray
    Write-Host "education -Setup" -ForegroundColor Yellow
    Write-Host ""
    Start-Sleep -Seconds 1
}

# メイン処理実行
Write-Host "🚀 起動中...`n" -ForegroundColor Gray
python $scriptPath

# 終了メッセージ
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
Write-Host ""
Write-Info "次回も .\education.ps1 で起動できます"
Write-Info "ヘルプ: .\education.ps1 -Help"
Write-Host ""
