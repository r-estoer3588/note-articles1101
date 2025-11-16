# LINE Bot Setup Helper Script
# Automates setup where possible

Write-Host "LINE Bot Setup Helper" -ForegroundColor Cyan
Write-Host "=" * 60

# 作業ディレクトリ確認
$currentDir = Get-Location
Write-Host "`n📁 作業ディレクトリ: $currentDir"

# 必要なファイルの存在確認
Write-Host "`n✅ ファイルチェック..." -ForegroundColor Yellow

$requiredFiles = @(
    "hogey_algorithm.py",
    "line_bot_helper.py",
    "n8n_workflow_menu_complete.json",
    "rich_menu_template.html",
    "QUICK_START_GUIDE.md"
)

$allFilesExist = $true
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file が見つかりません" -ForegroundColor Red
        $allFilesExist = $false
    }
}

if (-not $allFilesExist) {
    Write-Host "`n❌ 必要なファイルが不足しています" -ForegroundColor Red
    exit 1
}

# Python環境確認
Write-Host "`n🐍 Python環境チェック..." -ForegroundColor Yellow

try {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Pythonがインストールされていません" -ForegroundColor Red
    exit 1
}

# pandas確認
try {
    python -c "import pandas" 2>&1 | Out-Null
    Write-Host "  ✓ pandas インストール済み" -ForegroundColor Green
} catch {
    Write-Host "  ✗ pandas が必要です: pip install pandas" -ForegroundColor Red
    $installPandas = Read-Host "今すぐインストールしますか？ (y/n)"
    if ($installPandas -eq "y") {
        pip install pandas
    }
}

# ヘルパースクリプトテスト
Write-Host "`n🧪 ヘルパースクリプトテスト..." -ForegroundColor Yellow

try {
    $todayTheme = python line_bot_helper.py today_theme
    Write-Host "  ✓ 今日のテーマ: $todayTheme" -ForegroundColor Green
} catch {
    Write-Host "  ✗ ヘルパースクリプトエラー" -ForegroundColor Red
}

# hogey_algorithm.pyテスト
Write-Host "`n🧪 コアアルゴリズムテスト..." -ForegroundColor Yellow

try {
    python hogey_algorithm.py --count 1 --theme "テスト" --output setup_test.csv 2>&1 | Out-Null
    if (Test-Path "setup_test.csv") {
        Write-Host "  ✓ 投稿生成成功" -ForegroundColor Green
        Remove-Item "setup_test.csv" -Force
    } else {
        Write-Host "  ✗ 投稿生成失敗" -ForegroundColor Red
    }
} catch {
    Write-Host "  ✗ アルゴリズム実行エラー" -ForegroundColor Red
}

# リッチメニュー画像作成案内
Write-Host "`n🎨 リッチメニュー画像作成" -ForegroundColor Yellow
Write-Host "  1. rich_menu_template.html をブラウザで開きます"
Write-Host "  2. F12 → Ctrl+Shift+M でデバイスモード"
Write-Host "  3. サイズを 2500 x 1686 に設定"
Write-Host "  4. スクリーンショットを撮影して保存"

$openHtml = Read-Host "`nrich_menu_template.html を開きますか？ (y/n)"
if ($openHtml -eq "y") {
    Start-Process "rich_menu_template.html"
}

# Google Sheetsテンプレート案内
Write-Host "`n📊 Google Sheetsテンプレート" -ForegroundColor Yellow
Write-Host "  google_sheets_template.csv をGoogle Sheetsにインポートしてください"

$openTemplate = Read-Host "`nGoogle Sheetsをブラウザで開きますか？ (y/n)"
if ($openTemplate -eq "y") {
    Start-Process "https://docs.google.com/spreadsheets/"
}

# n8n起動案内
Write-Host "`n⚙️ n8n起動" -ForegroundColor Yellow
Write-Host "  n8nをインストールしていない場合:"
Write-Host "    npm install -g n8n"
Write-Host ""
Write-Host "  起動コマンド:"
Write-Host "    n8n start"

$startN8n = Read-Host "`nn8nを起動しますか？ (y/n)"
if ($startN8n -eq "y") {
    Write-Host "`nn8nを起動しています..." -ForegroundColor Cyan
    Write-Host "ブラウザで http://localhost:5678 が開きます"
    Write-Host "終了するには Ctrl+C を押してください"
    Write-Host ""
    Start-Process "http://localhost:5678"
    n8n start
}

# セットアップガイド案内
Write-Host "`n📘 次のステップ" -ForegroundColor Cyan
Write-Host "=" * 60
Write-Host ""
Write-Host "QUICK_START_GUIDE.md を開いて、以下を設定してください:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  ✓ 自動化完了: Python環境、ヘルパー関数"
Write-Host "  □ 手動設定: LINE Developers (15分)"
Write-Host "  □ 手動設定: Google Sheets (10分)"
Write-Host "  □ 手動設定: リッチメニュー (10分)"
Write-Host "  □ 手動設定: n8n設定 (15分)"
Write-Host ""

$openGuide = Read-Host "QUICK_START_GUIDE.md を開きますか？ (y/n)"
if ($openGuide -eq "y") {
    Start-Process "QUICK_START_GUIDE.md"
}

Write-Host "`n🎉 自動化できる部分のセットアップが完了しました！" -ForegroundColor Green
Write-Host "残りの手動設定はガイドに従って進めてください。" -ForegroundColor Cyan
