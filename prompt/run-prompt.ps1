#!/usr/bin/env pwsh
<#
.SYNOPSIS
    プロンプトファイルをコマンドラインから実行するスクリプト

.DESCRIPTION
    note-articles/prompt配下のプロンプトファイルを選択して、
    クリップボードにコピーまたは直接ChatGPTに投げる準備をします。

.PARAMETER PromptType
    実行するプロンプトの種類を指定
    - note: 記事構成設計プロンプト (note_prompt.txt)
    - product: 商品設計フレームワーク (product_design_prompt.txt)
    - video: AI動画収益化プロンプト (ai_video_monetization_prompt.txt)
    - all: すべてのプロンプトを表示

.PARAMETER Action
    実行するアクション
    - show: プロンプト内容を表示（デフォルト）
    - copy: クリップボードにコピー
    - open: デフォルトエディタで開く

.PARAMETER Section
    特定のセクションのみを表示/コピー（オプション）

.PARAMETER ArticleText
    リライトする記事本文（自動的にプロンプトの最後に追加されます）

.EXAMPLE
    .\run-prompt.ps1 -PromptType note -Action show
    記事構成設計プロンプトを表示

.EXAMPLE
    .\run-prompt.ps1 -PromptType product -Action copy
    商品設計プロンプトをクリップボードにコピー

.EXAMPLE
    .\run-prompt.ps1 -PromptType video -Action open
    動画収益化プロンプトをエディタで開く

.EXAMPLE
    .\run-prompt.ps1 -PromptType all
    すべてのプロンプトを一覧表示

.EXAMPLE
    .\run-prompt.ps1 -PromptType note -Action copy @'
    AIで書いたnote、なんか、つまらない。
    読んでも心動かない。なぜなのか。
    '@
    記事本文付きでプロンプトをコピー（ヒアドキュメント使用）

.EXAMPLE
    Get-Content article.txt | .\run-prompt.ps1 -PromptType note -Action copy
    ファイルから記事本文を読み込んでコピー
#>

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet('note', 'product', 'video', 'all')]
    [string]$PromptType = 'all',
    
    [Parameter(Mandatory=$false)]
    [ValidateSet('show', 'copy', 'open')]
    [string]$Action = 'show',
    
    [Parameter(Mandatory=$false)]
    [string]$Section = '',
    
    [Parameter(Mandatory=$false, ValueFromRemainingArguments=$true, ValueFromPipeline=$true)]
    [string[]]$ArticleText
)

begin {
    $allArticleText = @()
}

process {
    if ($ArticleText) {
        $allArticleText += $ArticleText
    }
}

end {

# スクリプトのディレクトリを取得
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# 記事本文を結合
$articleContent = if ($allArticleText) { $allArticleText -join "`n" } else { '' }

# カラー設定
$ColorTitle = 'Cyan'
$ColorSuccess = 'Green'
$ColorWarning = 'Yellow'
$ColorError = 'Red'
$ColorInfo = 'White'

# プロンプトファイルのマッピング
$PromptFiles = @{
    'note' = @{
        Path = Join-Path $ScriptDir 'note_prompt.txt'
        Name = '📝 記事構成設計プロンプト'
        Description = '読者が行動・購入・共感する記事構成を設計'
        Command = 'note'
    }
    'product' = @{
        Path = Join-Path $ScriptDir 'product_design_prompt.txt'
        Name = '🎯 商品設計フレームワーク'
        Description = 'ChatGPT活用型の商品設計（ペルソナ100個→商品案→コピー生成）'
        Command = 'product'
    }
    'video' = @{
        Path = Join-Path $ScriptDir 'ai_video_monetization_prompt.txt'
        Name = '🎬 AI動画×収益化フレームワーク'
        Description = 'AI動画生成からSNS集客、自動化までの完全ガイド'
        Command = 'video'
    }
}

# カラー設定
$ColorTitle = 'Cyan'
$ColorSuccess = 'Green'
$ColorWarning = 'Yellow'
$ColorError = 'Red'
$ColorInfo = 'White'

# ヘッダー表示
function Show-Header {
    Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor $ColorTitle
    Write-Host "   📚 Note Articles Prompt Runner" -ForegroundColor $ColorTitle
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor $ColorTitle
}

# プロンプト一覧表示
function Show-PromptList {
    Write-Host "利用可能なプロンプト:`n" -ForegroundColor $ColorInfo
    
    foreach ($key in $PromptFiles.Keys | Sort-Object) {
        $prompt = $PromptFiles[$key]
        $exists = Test-Path $prompt.Path
        $status = if ($exists) { "✅" } else { "❌" }
        
        Write-Host "  $status " -NoNewline
        Write-Host "$($prompt.Name)" -ForegroundColor $ColorSuccess
        Write-Host "      コマンド: " -NoNewline -ForegroundColor Gray
        Write-Host ".\run-prompt.ps1 -PromptType $($prompt.Command) -Action [show|copy|open]" -ForegroundColor $ColorWarning
        Write-Host "      説明: $($prompt.Description)" -ForegroundColor Gray
        Write-Host ""
    }
}

# プロンプト内容を表示
function Show-PromptContent {
    param([string]$FilePath, [string]$Name)
    
    if (-not (Test-Path $FilePath)) {
        Write-Host "❌ エラー: ファイルが見つかりません: $FilePath" -ForegroundColor $ColorError
        return $false
    }
    
    Write-Host "`n📄 $Name" -ForegroundColor $ColorSuccess
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor $ColorInfo
    
    $content = Get-Content $FilePath -Raw -Encoding UTF8
    
    if ($Section) {
        # 特定セクションのみ抽出（STEPまたは見出しで検索）
        $pattern = "(?ms)($Section.*?)(?=\n(STEP|━━━|📋|🎯|$))"
        if ($content -match $pattern) {
            Write-Host $matches[1]
        } else {
            Write-Host "⚠️  セクション '$Section' が見つかりませんでした" -ForegroundColor $ColorWarning
            Write-Host "全体を表示します...`n" -ForegroundColor $ColorWarning
            Write-Host $content
        }
    } else {
        Write-Host $content
    }
    
    Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor $ColorInfo
    Write-Host "✅ 表示完了: $Name`n" -ForegroundColor $ColorSuccess
    
    return $true
}

# クリップボードにコピー
function Copy-PromptToClipboard {
    param([string]$FilePath, [string]$Name, [string]$Article)
    
    if (-not (Test-Path $FilePath)) {
        Write-Host "❌ エラー: ファイルが見つかりません: $FilePath" -ForegroundColor $ColorError
        return $false
    }
    
    $content = Get-Content $FilePath -Raw -Encoding UTF8
    
    if ($Section) {
        $pattern = "(?ms)($Section.*?)(?=\n(STEP|━━━|📋|🎯|$))"
        if ($content -match $pattern) {
            $content = $matches[1]
        } else {
            Write-Host "⚠️  セクション '$Section' が見つかりませんでした" -ForegroundColor $ColorWarning
            Write-Host "全体をコピーします...`n" -ForegroundColor $ColorWarning
        }
    }
    
    # 記事本文が渡された場合、自動的に追加
    if ($Article) {
        $content += "`n`n【記事本文】`n$Article"
        Write-Host "✅ 記事本文を追加しました（$($Article.Length)文字）" -ForegroundColor $ColorSuccess
    }
    
    $content | Set-Clipboard
    
    Write-Host "`n✅ クリップボードにコピーしました: $Name" -ForegroundColor $ColorSuccess
    if ($Article) {
        Write-Host "   プロンプト + 記事本文がセットでコピーされています" -ForegroundColor $ColorInfo
    }
    Write-Host "   そのままChatGPTに貼り付けて使用できます`n" -ForegroundColor $ColorInfo
    
    return $true
}

# エディタで開く
function Open-PromptInEditor {
    param([string]$FilePath, [string]$Name)
    
    if (-not (Test-Path $FilePath)) {
        Write-Host "❌ エラー: ファイルが見つかりません: $FilePath" -ForegroundColor $ColorError
        return $false
    }
    
    Write-Host "`n📝 エディタで開いています: $Name" -ForegroundColor $ColorSuccess
    
    # VS Codeがあれば優先、なければデフォルトエディタ
    if (Get-Command code -ErrorAction SilentlyContinue) {
        code $FilePath
    } else {
        Start-Process $FilePath
    }
    
    Write-Host "✅ 開きました`n" -ForegroundColor $ColorSuccess
    
    return $true
}

# メイン処理
Show-Header

# すべてのプロンプトを表示
if ($PromptType -eq 'all') {
    Show-PromptList
    Write-Host "💡 使い方:" -ForegroundColor $ColorInfo
    Write-Host "   .\run-prompt.ps1 -PromptType <note|product|video> -Action <show|copy|open>`n" -ForegroundColor Gray
    exit 0
}

# 指定されたプロンプトを処理
$prompt = $PromptFiles[$PromptType]

if (-not $prompt) {
    Write-Host "❌ エラー: 不正なプロンプトタイプ: $PromptType" -ForegroundColor $ColorError
    Write-Host "   利用可能: note, product, video, all`n" -ForegroundColor $ColorWarning
    exit 1
}

switch ($Action) {
    'show' {
        $success = Show-PromptContent -FilePath $prompt.Path -Name $prompt.Name
        if ($articleContent) {
            Write-Host "`n📝 記事本文:" -ForegroundColor $ColorInfo
            Write-Host $articleContent
        }
    }
    'copy' {
        $success = Copy-PromptToClipboard -FilePath $prompt.Path -Name $prompt.Name -Article $articleContent
    }
    'open' {
        $success = Open-PromptInEditor -FilePath $prompt.Path -Name $prompt.Name
        if ($articleContent) {
            Write-Host "⚠️  記事本文は -Action open では使用されません" -ForegroundColor $ColorWarning
        }
    }
}

if (-not $success) {
    exit 1
}

# 使い方のヒント
Write-Host "💡 次のステップ:" -ForegroundColor $ColorInfo
if ($articleContent) {
    Write-Host "   1. ChatGPTに貼り付け（プロンプト+記事本文がセット済み）" -ForegroundColor Gray
    Write-Host "   2. ChatGPTの出力を受け取る`n" -ForegroundColor Gray
} else {
    Write-Host "   1. コピーしたプロンプトをChatGPTに貼り付け" -ForegroundColor Gray
    Write-Host "   2. 記事本文や商品情報を追加入力" -ForegroundColor Gray
    Write-Host "   3. ChatGPTの出力を受け取る`n" -ForegroundColor Gray
}

} # end block の閉じ括弧
