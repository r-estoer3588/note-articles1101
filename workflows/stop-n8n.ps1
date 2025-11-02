# n8n Notes Organizer - 停止スクリプト
# 設定は保持されたまま、コンテナだけ停止します

Write-Host '🛑 n8n Notes Organizer を停止します...' -ForegroundColor Yellow

# スクリプトのディレクトリに移動
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# docker-compose.ymlが存在するか確認
if (-not (Test-Path 'docker-compose.yml')) {
    Write-Host '❌ エラー: docker-compose.yml が見つかりません' -ForegroundColor Red
    Write-Host '   workflows/ ディレクトリで実行してください' -ForegroundColor Yellow
    exit 1
}

# ボリュームを削除するか確認
Write-Host ''
Write-Host '⚠️  注意: 設定を保持したまま停止しますか? (推奨)' -ForegroundColor Yellow
Write-Host '   Y = 設定を保持して停止(推奨)' -ForegroundColor Green
Write-Host '   N = 設定を全て削除して停止' -ForegroundColor Red
Write-Host ''
Write-Host '選択してください (Y/n): ' -NoNewline -ForegroundColor White
$response = Read-Host

if ($response -eq 'n' -or $response -eq 'N') {
    Write-Host ''
    Write-Host '⚠️  本当に設定を削除しますか?' -ForegroundColor Red
    Write-Host '   これを実行すると、ワークフローとAPIキーが全て削除されます' -ForegroundColor Yellow
    Write-Host ''
    Write-Host '削除する場合は DELETE と入力してください: ' -NoNewline -ForegroundColor White
    $confirm = Read-Host
    
    if ($confirm -eq 'DELETE') {
        Write-Host ''
        Write-Host '🗑️  設定を削除してコンテナを停止中...' -ForegroundColor Red
        docker-compose down -v
        Write-Host ''
        Write-Host '✅ 設定を含めて全て削除されました' -ForegroundColor Yellow
        Write-Host '   次回起動時は初回セットアップが必要です' -ForegroundColor Cyan
    } else {
        Write-Host ''
        Write-Host '❌ キャンセルされました(何も変更されていません)' -ForegroundColor Green
        exit 0
    }
} else {
    # 設定を保持して停止
    Write-Host ''
    Write-Host '💾 設定を保持してコンテナを停止中...' -ForegroundColor Cyan
    docker-compose down
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ''
        Write-Host '✅ n8n が停止しました' -ForegroundColor Green
        Write-Host '   設定は保存されています' -ForegroundColor Cyan
        Write-Host ''
        Write-Host '🚀 再起動するには:' -ForegroundColor White
        Write-Host '   .\start-n8n.ps1' -ForegroundColor Yellow
        Write-Host ''
        Write-Host '   または' -ForegroundColor White
        Write-Host '   docker-compose up -d' -ForegroundColor Yellow
    } else {
        Write-Host ''
        Write-Host '❌ エラー: 停止に失敗しました' -ForegroundColor Red
        exit 1
    }
}
