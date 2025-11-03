#!/usr/bin/env pwsh
<#
.SYNOPSIS
    ChatGPTの出力からnote投稿用Markdownファイルを生成

.DESCRIPTION
    ChatGPTでリライトした記事を、note投稿用のMarkdown形式に整形して保存します。

.PARAMETER InputText
    ChatGPTの出力テキスト（クリップボードまたはファイルから）

.PARAMETER OutputDir
    保存先ディレクトリ（デフォルト: drafts）

.PARAMETER Title
    記事タイトル（自動抽出も可能）

.PARAMETER AutoOpen
    保存後に自動的にファイルを開く

.EXAMPLE
    Get-Clipboard | .\save-note-article.ps1
    クリップボードからChatGPT出力を読み込んでMarkdown保存

.EXAMPLE
    .\save-note-article.ps1 -InputText (Get-Content chatgpt_output.txt -Raw)
    ファイルから読み込んで保存

.EXAMPLE
    Get-Clipboard | .\save-note-article.ps1 -Title "AI動画で稼ぐ方法" -AutoOpen
    タイトル指定 + 自動的にファイルを開く
#>

param(
    [Parameter(Mandatory=$false, ValueFromPipeline=$true)]
    [string]$InputText,
    
    [Parameter(Mandatory=$false)]
    [string]$OutputDir = 'drafts',
    
    [Parameter(Mandatory=$false)]
    [string]$Title = '',
    
    [Parameter(Mandatory=$false)]
    [switch]$AutoOpen
)

begin {
    $allInputText = @()
}

process {
    if ($InputText) {
        $allInputText += $InputText
    }
}

end {

# スクリプトのディレクトリを取得
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RootDir = Split-Path -Parent $ScriptDir  # note-articles ルート

# カラー設定
$ColorTitle = 'Cyan'
$ColorSuccess = 'Green'
$ColorWarning = 'Yellow'
$ColorError = 'Red'
$ColorInfo = 'White'

Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor $ColorTitle
Write-Host "   📝 Note Article Generator" -ForegroundColor $ColorTitle
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor $ColorTitle

# 入力テキストを結合
$content = $allInputText -join "`n"

if (-not $content) {
    # クリップボードから取得を試みる
    Write-Host "📋 クリップボードから取得を試みています..." -ForegroundColor $ColorInfo
    $content = Get-Clipboard -Raw -ErrorAction SilentlyContinue
    
    if (-not $content) {
        Write-Host "❌ エラー: 入力テキストがありません" -ForegroundColor $ColorError
        Write-Host "   使い方: Get-Clipboard | .\save-note-article.ps1`n" -ForegroundColor $ColorWarning
        exit 1
    }
}

Write-Host "✅ 入力テキストを取得しました（$($content.Length)文字）`n" -ForegroundColor $ColorSuccess

# タイトルを抽出（指定がない場合）
if (-not $Title) {
    # ChatGPT出力から「タイトル案」セクションを探す
    if ($content -match '(?:タイトル案|【タイトル】|#\s*タイトル).*?[：:]\s*(.+?)(?:\n|$)') {
        $Title = $matches[1].Trim()
        Write-Host "📌 タイトルを自動抽出: $Title" -ForegroundColor $ColorInfo
    } else {
        # 最初の見出しを使用
        if ($content -match '^#\s*(.+?)$' -or $content -match '【(.+?)】') {
            $Title = $matches[1].Trim()
            Write-Host "📌 最初の見出しをタイトルに: $Title" -ForegroundColor $ColorInfo
        } else {
            # デフォルトタイトル
            $Title = "新規記事_$(Get-Date -Format 'yyyyMMdd_HHmm')"
            Write-Host "⚠️  タイトルが見つからないため自動生成: $Title" -ForegroundColor $ColorWarning
        }
    }
}

# ファイル名用にサニタイズ
$safeTitleForFilename = $Title -replace '[\\/:*?"<>|]', '_'
$safeTitleForFilename = $safeTitleForFilename -replace '\s+', '_'
$safeTitleForFilename = $safeTitleForFilename.Substring(0, [Math]::Min(50, $safeTitleForFilename.Length))

# 出力ディレクトリを作成
$outputPath = Join-Path $RootDir $OutputDir
if (-not (Test-Path $outputPath)) {
    New-Item -Path $outputPath -ItemType Directory -Force | Out-Null
    Write-Host "📁 ディレクトリを作成: $outputPath" -ForegroundColor $ColorInfo
}

# ファイル名を生成
$timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$filename = "${timestamp}_${safeTitleForFilename}.md"
$fullPath = Join-Path $outputPath $filename

# note用のMarkdown形式に整形
$noteMarkdown = @"
---
title: $Title
created: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
source: ChatGPT (note-articles prompt)
---

# $Title

$content

---

## メタ情報
- 作成日時: $(Get-Date -Format 'yyyy年MM月dd日 HH:mm')
- 生成元: note_prompt.txt
- ステータス: 下書き

## 次のアクション
- [ ] タイトルの最終確認
- [ ] 本文の誤字脱字チェック
- [ ] noteに投稿
- [ ] SNSでシェア
"@

# ファイルに保存
$noteMarkdown | Out-File -FilePath $fullPath -Encoding UTF8

Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor $ColorSuccess
Write-Host "✅ Markdownファイルを保存しました!" -ForegroundColor $ColorSuccess
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor $ColorSuccess

Write-Host "📄 ファイル名: $filename" -ForegroundColor $ColorInfo
Write-Host "📂 保存場所: $fullPath" -ForegroundColor $ColorInfo
Write-Host "📏 文字数: $($content.Length) 文字`n" -ForegroundColor $ColorInfo

# 相対パスを表示
$relativePath = $fullPath.Replace($RootDir + '\', '')
Write-Host "💡 相対パス: $relativePath`n" -ForegroundColor $ColorWarning

# 自動的に開く
if ($AutoOpen) {
    Write-Host "📝 ファイルを開いています..." -ForegroundColor $ColorInfo
    
    if (Get-Command code -ErrorAction SilentlyContinue) {
        code $fullPath
        Write-Host "✅ VS Codeで開きました`n" -ForegroundColor $ColorSuccess
    } else {
        Start-Process $fullPath
        Write-Host "✅ デフォルトエディタで開きました`n" -ForegroundColor $ColorSuccess
    }
}

# 次のステップを表示
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor $ColorTitle
Write-Host "📋 次のステップ" -ForegroundColor $ColorTitle
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor $ColorTitle

Write-Host "1️⃣  ファイルを確認・編集:" -ForegroundColor $ColorInfo
Write-Host "   code `"$fullPath`"`n" -ForegroundColor Gray

Write-Host "2️⃣  noteに投稿:" -ForegroundColor $ColorInfo
Write-Host "   https://note.com/new" -ForegroundColor Gray
Write-Host "   → ファイルの内容をコピー&ペースト`n" -ForegroundColor Gray

Write-Host "3️⃣  完了後は drafts → articles に移動:" -ForegroundColor $ColorInfo
Write-Host "   Move-Item `"$fullPath`" `"$RootDir\articles\`"`n" -ForegroundColor Gray

# サマリー
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor $ColorSuccess
Write-Host "🎉 記事の準備が完了しました!" -ForegroundColor $ColorSuccess
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor $ColorSuccess

} # end block の閉じ括弧
