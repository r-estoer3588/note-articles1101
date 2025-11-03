#!/usr/bin/env pwsh
<#
.SYNOPSIS
    note記事のリライト→保存までを一気通貫で実行

.DESCRIPTION
    1. プロンプトと記事本文をChatGPTに送信（クリップボード経由）
    2. ChatGPTの出力を取得
    3. note投稿用Markdownに整形して保存

.PARAMETER ArticleFile
    リライトする記事ファイル（.txt または .md）

.PARAMETER Title
    記事タイトル（省略可）

.PARAMETER AutoOpen
    保存後に自動的にファイルを開く

.EXAMPLE
    .\note-workflow.ps1 -ArticleFile draft.txt
    記事ファイルを指定してリライト

.EXAMPLE
    .\note-workflow.ps1 -ArticleFile draft.txt -Title "AI動画で稼ぐ" -AutoOpen
    タイトル指定 + 自動オープン

.EXAMPLE
    Get-Clipboard | .\note-workflow.ps1
    クリップボードの記事をリライト
#>

param(
    [Parameter(Mandatory=$false, ValueFromPipeline=$true)]
    [string]$ArticleFile,
    
    [Parameter(Mandatory=$false)]
    [string]$Title = '',
    
    [Parameter(Mandatory=$false)]
    [switch]$AutoOpen
)

begin {
    $allInput = @()
}

process {
    if ($ArticleFile) {
        $allInput += $ArticleFile
    }
}

end {

# スクリプトのディレクトリを取得
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# カラー設定
$ColorTitle = 'Cyan'
$ColorSuccess = 'Green'
$ColorWarning = 'Yellow'
$ColorError = 'Red'
$ColorInfo = 'White'

Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor $ColorTitle
Write-Host "   🚀 Note Workflow Automation" -ForegroundColor $ColorTitle
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor $ColorTitle

# STEP 1: 記事本文を取得
$articleContent = ''

if ($allInput) {
    $inputPath = $allInput -join ' '
    
    # ファイルパスとして扱う
    if (Test-Path $inputPath) {
        Write-Host "📄 ファイルから記事を読み込んでいます: $inputPath" -ForegroundColor $ColorInfo
        $articleContent = Get-Content $inputPath -Raw -Encoding UTF8
        Write-Host "✅ 読み込み完了（$($articleContent.Length)文字）`n" -ForegroundColor $ColorSuccess
    } else {
        # テキストとして扱う
        $articleContent = $inputPath
        Write-Host "📝 入力テキストを取得しました（$($articleContent.Length)文字）`n" -ForegroundColor $ColorSuccess
    }
} else {
    # クリップボードから取得
    Write-Host "📋 クリップボードから記事を読み込んでいます..." -ForegroundColor $ColorInfo
    $articleContent = Get-Clipboard -Raw -ErrorAction SilentlyContinue
    
    if (-not $articleContent) {
        Write-Host "❌ エラー: 記事本文がありません" -ForegroundColor $ColorError
        Write-Host "   使い方: .\note-workflow.ps1 -ArticleFile draft.txt`n" -ForegroundColor $ColorWarning
        exit 1
    }
    
    Write-Host "✅ クリップボードから取得しました（$($articleContent.Length)文字）`n" -ForegroundColor $ColorSuccess
}

# STEP 2: プロンプト + 記事本文をクリップボードにコピー
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor $ColorTitle
Write-Host "STEP 1: プロンプト準備" -ForegroundColor $ColorTitle
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor $ColorTitle

Write-Host "🔄 note_prompt.txt + 記事本文をクリップボードにコピー中..." -ForegroundColor $ColorInfo

# run-prompt.ps1を実行（記事本文を渡す）
$runPromptScript = Join-Path $ScriptDir "run-prompt.ps1"
echo $articleContent | & $runPromptScript -PromptType note -Action copy

Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor $ColorWarning
Write-Host "⏸️  手動操作が必要です" -ForegroundColor $ColorWarning
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor $ColorWarning

Write-Host "次の手順を実行してください:`n" -ForegroundColor $ColorInfo
Write-Host "1️⃣  ChatGPTを開く: https://chat.openai.com/" -ForegroundColor $ColorSuccess
Write-Host "2️⃣  Ctrl+V でプロンプトを貼り付け" -ForegroundColor $ColorSuccess
Write-Host "3️⃣  Enter で実行" -ForegroundColor $ColorSuccess
Write-Host "4️⃣  出力された【全文リライト案】をすべてコピー (Ctrl+A → Ctrl+C)" -ForegroundColor $ColorSuccess
Write-Host "5️⃣  このウィンドウに戻って Enter を押す`n" -ForegroundColor $ColorSuccess

Write-Host "準備ができたら Enter キーを押してください..." -ForegroundColor $ColorWarning
Read-Host

# STEP 3: ChatGPTの出力を取得
Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor $ColorTitle
Write-Host "STEP 2: ChatGPT出力を取得" -ForegroundColor $ColorTitle
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor $ColorTitle

Write-Host "📋 クリップボードからChatGPTの出力を取得しています..." -ForegroundColor $ColorInfo
$chatgptOutput = Get-Clipboard -Raw

if (-not $chatgptOutput -or $chatgptOutput.Length -lt 100) {
    Write-Host "❌ エラー: ChatGPTの出力が取得できませんでした" -ForegroundColor $ColorError
    Write-Host "   クリップボードに出力がコピーされているか確認してください`n" -ForegroundColor $ColorWarning
    exit 1
}

Write-Host "✅ ChatGPTの出力を取得しました（$($chatgptOutput.Length)文字）`n" -ForegroundColor $ColorSuccess

# STEP 4: Markdownファイルに保存
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor $ColorTitle
Write-Host "STEP 3: Markdownファイルに保存" -ForegroundColor $ColorTitle
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor $ColorTitle

# save-note-article.ps1を実行
$saveScript = Join-Path $ScriptDir "save-note-article.ps1"

if ($Title) {
    echo $chatgptOutput | & $saveScript -Title $Title -AutoOpen:$AutoOpen
} else {
    echo $chatgptOutput | & $saveScript -AutoOpen:$AutoOpen
}

Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor $ColorSuccess
Write-Host "🎉 すべての処理が完了しました!" -ForegroundColor $ColorSuccess
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor $ColorSuccess

Write-Host "💡 次のアクション:" -ForegroundColor $ColorInfo
Write-Host "   1. drafts フォルダ内の Markdown ファイルを確認" -ForegroundColor Gray
Write-Host "   2. note.com で記事を投稿" -ForegroundColor Gray
Write-Host "   3. 投稿完了後、ファイルを articles フォルダに移動`n" -ForegroundColor Gray

} # end block の閉じ括弧
