# Threads画像生成ツールの実行スクリプト

# 1. 依存ライブラリのチェックとインストール
Write-Host "📦 依存ライブラリをチェックしています..."
pip install google-generativeai Pillow

# 2. 入力ファイルの確認
$InputFile = "input/threads_image_prompts.txt"
if (-not (Test-Path $InputFile)) {
    Write-Error "❌ 入力ファイルが見つかりません: $InputFile"
    exit 1
}

# 3. 出力ディレクトリの作成
$OutputDir = "outputs/threads_images_$(Get-Date -Format 'yyyyMMdd_HHmm')"
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

# 4. 実行
Write-Host "🚀 画像生成を開始します..."
Write-Host "   入力: $InputFile"
Write-Host "   出力: $OutputDir"

# APIキーの確認 (環境変数がなければ入力を促す)
if (-not $env:GOOGLE_API_KEY) {
    Write-Warning "⚠️ GOOGLE_API_KEY 環境変数が設定されていません。"
    $ApiKey = Read-Host "Google API Keyを入力してください (入力しない場合はプロンプト生成のみスキップされます)"
    if ($ApiKey) {
        $env:GOOGLE_API_KEY = $ApiKey
    }
}

# スクリプト実行
python tools/generate_threads_images.py --input $InputFile --out-dir $OutputDir

Write-Host "✅ 完了しました。出力フォルダを確認してください: $OutputDir"
Start-Process $OutputDir
