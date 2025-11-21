# Threads画像生成ツールの実行スクリプト

param (
    [string]$InputFile = "input/threads_image_prompts.txt",
    [switch]$Test
)

# 1. 依存ライブラリのチェックとインストール
Write-Host "📦 依存ライブラリをチェックしています..."
pip install google-generativeai Pillow python-dotenv

# 2. 入力ファイルの確認
if ($Test) {
    $InputFile = "input/test_single_prompt.txt"
}

if (-not (Test-Path $InputFile)) {
    Write-Error "❌ 入力ファイルが見つかりません: $InputFile"
    exit 1
}

# 3. 出力ディレクトリの作成
$OutputDir = "outputs/threads_images_$(Get-Date -Format 'yyyyMMdd_HHmm')"
if ($Test) {
    $OutputDir = "outputs/test_single_$(Get-Date -Format 'yyyyMMdd_HHmm')"
}
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

# 4. 実行
Write-Host "🚀 画像生成を開始します..."
Write-Host "   入力: $InputFile"
Write-Host "   出力: $OutputDir"

# APIキーの確認 (環境変数がなければ入力を促す)
# .envファイルもチェック
$EnvFile = "tools/.env"
$HasApiKey = $env:GOOGLE_API_KEY
if (-not $HasApiKey -and (Test-Path $EnvFile)) {
    $EnvContent = Get-Content $EnvFile
    if ($EnvContent -match "GOOGLE_API_KEY=.+") {
        # 簡易チェック: 値が入っているか
        $HasApiKey = $true
    }
}

if (-not $HasApiKey) {
    Write-Warning "⚠️ GOOGLE_API_KEY 環境変数が設定されておらず、tools/.env にも記述がありません。"
    Write-Warning "   tools/.env ファイルを開いて GOOGLE_API_KEY を設定することをお勧めします。"
    $ApiKey = Read-Host "Google API Keyを入力してください (入力しない場合はプロンプト生成のみスキップされます)"
    if ($ApiKey) {
        $env:GOOGLE_API_KEY = $ApiKey
    }
}

# スクリプト実行
python tools/generate_threads_images.py --input $InputFile --out-dir $OutputDir

Write-Host "✅ 完了しました。出力フォルダを確認してください: $OutputDir"
Start-Process $OutputDir
