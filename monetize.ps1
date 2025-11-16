# monetize.ps1 - SNSマネタイズプラン生成ツール ランチャー
#
# 使い方:
#   monetize              # 対話型でSTEP1質問に回答
#   monetize -Api         # OpenAI APIで自動プラン生成
#   monetize -Help        # ヘルプ表示
#   monetize -Setup       # 初回セットアップ

param(
    [switch]$Help,
    [switch]$Setup,
    [switch]$Api,
    [switch]$PromptOnly,
    [string]$Load
)

$ErrorActionPreference = "Stop"

# =============================================================================
# カラー出力関数
# =============================================================================

function Write-Header {
    param([string]$Text)
    Write-Host ""
    Write-Host ("=" * 60) -ForegroundColor Magenta
    Write-Host $Text -ForegroundColor Magenta -NoNewline
    Write-Host ""
    Write-Host ("=" * 60) -ForegroundColor Magenta
    Write-Host ""
}

function Write-Success {
    param([string]$Text)
    Write-Host "✓ $Text" -ForegroundColor Green
}

function Write-Warning-Custom {
    param([string]$Text)
    Write-Host "⚠ $Text" -ForegroundColor Yellow
}

function Write-Info {
    param([string]$Text)
    Write-Host "ℹ $Text" -ForegroundColor Cyan
}

function Write-Error-Custom {
    param([string]$Text)
    Write-Host "✗ $Text" -ForegroundColor Red
}

# =============================================================================
# ヘルプ表示
# =============================================================================

if ($Help) {
    Write-Header "💰 SNSマネタイズプラン生成ツール"
    
    Write-Host "このツールは、あなたの人生を変える本気のSNSマネタイズプランを設計します。" -ForegroundColor White
    Write-Host ""
    Write-Host "【使い方】" -ForegroundColor Yellow
    Write-Host "  monetize              # 対話型でSTEP1質問に回答" -ForegroundColor White
    Write-Host "  monetize -Api         # OpenAI APIで自動プラン生成" -ForegroundColor White
    Write-Host "  monetize -PromptOnly  # プロンプトのみ生成" -ForegroundColor White
    Write-Host "  monetize -Load data.json -Api  # 保存済み回答からプラン生成" -ForegroundColor White
    Write-Host "  monetize -Help        # このヘルプ" -ForegroundColor White
    Write-Host "  monetize -Setup       # 初回セットアップ" -ForegroundColor White
    Write-Host ""
    Write-Host "【エイリアス】" -ForegroundColor Yellow
    Write-Host "  mz                    # 短縮形" -ForegroundColor White
    Write-Host ""
    Write-Host "【STEP1: 現状の深掘り分析】" -ForegroundColor Yellow
    Write-Host "  5つのカテゴリ、計20以上の質問に答える形で、" -ForegroundColor White
    Write-Host "  あなたの状況を深く理解します：" -ForegroundColor White
    Write-Host "  1. 現在の状況（職業、収入、SNS運用歴など）" -ForegroundColor Gray
    Write-Host "  2. スキル・経験の棚卸し" -ForegroundColor Gray
    Write-Host "  3. リソース確認" -ForegroundColor Gray
    Write-Host "  4. 目標とマインド" -ForegroundColor Gray
    Write-Host "  5. 過去の失敗・課題" -ForegroundColor Gray
    Write-Host ""
    Write-Host "【STEP2: 戦略設計】" -ForegroundColor Yellow
    Write-Host "  STEP1の回答をもとに、以下を含む包括的プランを生成：" -ForegroundColor White
    Write-Host "  ・最強ポジション分析" -ForegroundColor Gray
    Write-Host "  ・ターゲット顧客の明確化" -ForegroundColor Gray
    Write-Host "  ・SNS戦略（プラットフォーム別）" -ForegroundColor Gray
    Write-Host "  ・マネタイズ戦略（即金型/積み上げ型/資産型）" -ForegroundColor Gray
    Write-Host "  ・90日実行プラン（週次タスク）" -ForegroundColor Gray
    Write-Host "  ・コンテンツ戦略（バズる投稿テンプレート）" -ForegroundColor Gray
    Write-Host "  ・収益目標とKPI" -ForegroundColor Gray
    Write-Host "  ・よくある失敗と回避策" -ForegroundColor Gray
    Write-Host "  ・リスクヘッジ戦略" -ForegroundColor Gray
    Write-Host "  ・あなた専用の成功の方程式" -ForegroundColor Gray
    Write-Host ""
    Write-Host "【出力ファイル】" -ForegroundColor Yellow
    Write-Host "  outputs/monetize/" -ForegroundColor White
    Write-Host "    ├─ step1_answers_YYYYMMDD_HHMMSS.json  # 回答データ" -ForegroundColor Gray
    Write-Host "    ├─ prompt_YYYYMMDD_HHMMSS.txt          # 生成プロンプト" -ForegroundColor Gray
    Write-Host "    └─ monetize_plan_YYYYMMDD_HHMMSS.md    # 最終プラン" -ForegroundColor Gray
    Write-Host ""
    Write-Host "【OpenAI API使用】" -ForegroundColor Yellow
    Write-Host "  -Api オプションで自動生成する場合、環境変数が必要：" -ForegroundColor White
    Write-Host "  `$env:OPENAI_API_KEY = 'sk-...'" -ForegroundColor Gray
    Write-Host ""
    Write-Host "【GitHub Copilot Chat統合】" -ForegroundColor Yellow
    Write-Host "  -PromptOnly オプションで生成したプロンプトを" -ForegroundColor White
    Write-Host "  GitHub Copilot Chatに貼り付けて使用可能" -ForegroundColor White
    Write-Host ""
    Write-Info "詳細: C:\Repos\note-articles\tools\monetize_planner.py"
    
    exit 0
}

# =============================================================================
# セットアップ
# =============================================================================

if ($Setup) {
    Write-Header "🔧 SNSマネタイズツール セットアップ"
    
    Write-Info "環境をチェックしています..."
    
    # Python確認
    try {
        $pythonVersion = python --version 2>&1
        Write-Success "Python: $pythonVersion"
    }
    catch {
        Write-Error-Custom "Pythonがインストールされていません"
        Write-Info "https://www.python.org/downloads/ からインストールしてください"
        exit 1
    }
    
    # 依存パッケージ確認
    Write-Info "依存パッケージを確認中..."
    
    $packages = @("openai", "pyperclip")
    $missingPackages = @()
    
    foreach ($pkg in $packages) {
        try {
            python -c "import $pkg" 2>$null
            Write-Success "${pkg}: インストール済み"
        }
        catch {
            Write-Warning-Custom "${pkg}: 未インストール"
            $missingPackages += $pkg
        }
    }
    
    # インストール提案
    if ($missingPackages.Count -gt 0) {
        Write-Host ""
        Write-Warning-Custom "以下のパッケージがインストールされていません："
        foreach ($pkg in $missingPackages) {
            Write-Host "  - $pkg" -ForegroundColor Yellow
        }
        Write-Host ""
        Write-Info "インストールしますか？ (y/n)"
        $response = Read-Host
        
        if ($response -eq "y") {
            Write-Info "パッケージをインストール中..."
            pip install $($missingPackages -join " ")
            Write-Success "インストール完了"
        }
        else {
            Write-Warning-Custom "スキップしました"
            Write-Info "手動インストール: pip install openai pyperclip"
        }
    }
    
    # OpenAI API Key確認
    Write-Host ""
    Write-Info "OpenAI API設定を確認中..."
    
    if ($env:OPENAI_API_KEY) {
        $keyPreview = $env:OPENAI_API_KEY.Substring(0, [Math]::Min(10, $env:OPENAI_API_KEY.Length)) + "..."
        Write-Success "OPENAI_API_KEY: 設定済み ($keyPreview)"
    }
    else {
        Write-Warning-Custom "OPENAI_API_KEY: 未設定"
        Write-Info "OpenAI APIで自動生成する場合は設定が必要です"
        Write-Host ""
        Write-Info "API Keyを設定しますか？ (y/n)"
        $response = Read-Host
        
        if ($response -eq "y") {
            Write-Info "OpenAI API Keyを入力してください："
            $apiKey = Read-Host -AsSecureString
            $apiKeyPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
                [Runtime.InteropServices.Marshal]::SecureStringToBSTR($apiKey)
            )
            
            # 現在のセッションに設定
            $env:OPENAI_API_KEY = $apiKeyPlain
            Write-Success "現在のセッションに設定しました"
            
            Write-Info "永続化しますか？（PowerShellプロファイルに追加） (y/n)"
            $persist = Read-Host
            
            if ($persist -eq "y") {
                $profilePath = $PROFILE
                if (-not (Test-Path $profilePath)) {
                    New-Item -Path $profilePath -ItemType File -Force | Out-Null
                }
                
                Add-Content -Path $profilePath -Value "`n# OpenAI API Key for Monetize Tool"
                Add-Content -Path $profilePath -Value "`$env:OPENAI_API_KEY = '$apiKeyPlain'"
                
                Write-Success "プロファイルに追加しました: $profilePath"
            }
        }
        else {
            Write-Info "GitHub Copilot Chat統合モードをお勧めします（-PromptOnly）"
        }
    }
    
    # 出力ディレクトリ作成
    Write-Host ""
    Write-Info "出力ディレクトリを準備中..."
    $projectRoot = "C:\Repos\note-articles"
    $outputDir = Join-Path $projectRoot "outputs\monetize"
    
    if (-not (Test-Path $outputDir)) {
        New-Item -Path $outputDir -ItemType Directory -Force | Out-Null
        Write-Success "作成しました: $outputDir"
    }
    else {
        Write-Success "存在を確認: $outputDir"
    }
    
    Write-Host ""
    Write-Header "✅ セットアップ完了"
    Write-Success "monetize ツールを使用する準備ができました"
    Write-Info "次のコマンド: monetize"
    
    exit 0
}

# =============================================================================
# メイン実行
# =============================================================================

Write-Header "💰 SNSマネタイズプラン生成"

# プロジェクトルート確認
$projectRoot = "C:\Repos\note-articles"
$scriptPath = Join-Path $projectRoot "tools\monetize_planner.py"

if (-not (Test-Path $scriptPath)) {
    Write-Error-Custom "スクリプトが見つかりません: $scriptPath"
    Write-Info "セットアップを実行してください: monetize -Setup"
    exit 1
}

# Python確認
try {
    python --version | Out-Null
}
catch {
    Write-Error-Custom "Pythonが見つかりません"
    Write-Info "セットアップを実行してください: monetize -Setup"
    exit 1
}

try {
    # プロジェクトルートに移動
    Push-Location $projectRoot
    
    # 引数構築
    $pythonArgs = @("tools\monetize_planner.py")
    
    if ($Api) {
        $pythonArgs += "--api"
    }
    
    if ($PromptOnly) {
        $pythonArgs += "--prompt-only"
    }
    
    if ($Load) {
        $pythonArgs += "--load"
        $pythonArgs += $Load
    }
    
    # 実行
    Write-Info "ツールを起動中..."
    Write-Host ""
    
    & python $pythonArgs
    
    $exitCode = $LASTEXITCODE
    
    Write-Host ""
    if ($exitCode -eq 0) {
        Write-Success "完了しました"
        Write-Info "出力: $projectRoot\outputs\monetize\"
    }
    else {
        Write-Warning-Custom "エラーで終了しました（終了コード: $exitCode）"
    }
}
catch {
    Write-Error-Custom "実行エラー: $_"
    Write-Info "詳細ログ: python tools\monetize_planner.py"
    exit 1
}
finally {
    # 元のディレクトリに戻る
    Pop-Location
}
