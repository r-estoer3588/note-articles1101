# n8n Notes Organizer - 起動スクリプト
# 設定は永久保存されているので、このスクリプトを実行するだけでOK

Write-Host '🚀 n8n Notes Organizer を起動します...' -ForegroundColor Green

# スクリプトのディレクトリに移動
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# Dockerが起動しているか確認
$dockerRunning = docker info 2>$null
if (-not $?) {
    Write-Host '❌ エラー: Dockerが起動していません' -ForegroundColor Red
    Write-Host '   Docker Desktopを起動してから再実行してください' -ForegroundColor Yellow
    exit 1
}

# docker-compose.ymlが存在するか確認
if (-not (Test-Path 'docker-compose.yml')) {
    Write-Host '❌ エラー: docker-compose.yml が見つかりません' -ForegroundColor Red
    Write-Host '   workflows/ ディレクトリで実行してください' -ForegroundColor Yellow
    exit 1
}

# n8nコンテナを起動
Write-Host '📦 n8nコンテナを起動中...' -ForegroundColor Cyan
docker-compose up -d

if ($LASTEXITCODE -eq 0) {
    Write-Host ''
    Write-Host '✅ n8n が起動しました!' -ForegroundColor Green
    Write-Host ''
    Write-Host '🌐 ブラウザで以下にアクセスしてください:' -ForegroundColor White
    Write-Host '   http://localhost:5678' -ForegroundColor Yellow
    Write-Host ''
    Write-Host '🔑 ログイン情報:' -ForegroundColor White
    Write-Host '   ユーザー名: admin' -ForegroundColor Yellow
    Write-Host '   パスワード: docker-compose.yml を確認' -ForegroundColor Yellow
    Write-Host ''
    Write-Host '💡 初回のみ:' -ForegroundColor White
    Write-Host '   1. notes-to-notion-auto-organizer.json をインポート' -ForegroundColor Cyan
    Write-Host '   2. OpenAI/Notion API キーを設定' -ForegroundColor Cyan
    Write-Host '   3. ワークフローをActiveにする' -ForegroundColor Cyan
    Write-Host ''
    Write-Host '🎉 以降は設定不要です!' -ForegroundColor Green
    Write-Host ''
    
    # コンテナのログを表示するか確認
    Write-Host 'ログを表示しますか? (y/N): ' -NoNewline -ForegroundColor White
    $response = Read-Host
    if ($response -eq 'y' -or $response -eq 'Y') {
        docker-compose logs -f n8n
    }
} else {
    Write-Host ''
    Write-Host '❌ エラー: n8nの起動に失敗しました' -ForegroundColor Red
    Write-Host '   以下のコマンドでログを確認してください:' -ForegroundColor Yellow
    Write-Host '   docker-compose logs n8n' -ForegroundColor Cyan
    exit 1
}
