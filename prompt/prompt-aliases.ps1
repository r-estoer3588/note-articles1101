# Note Articles Prompt Runner - Quick Aliases
# このファイルをPowerShellプロファイルに追加すると、短いコマンドで実行できます

# プロンプトディレクトリのパス（環境に応じて変更してください）
$PROMPT_DIR = "C:\Repos\note-articles\prompt"

# エイリアス関数定義

function prompt-note {
    <#
    .SYNOPSIS
        記事構成設計プロンプトを実行
    .PARAMETER Action
        show, copy, open のいずれか（デフォルト: copy）
    #>
    param([string]$Action = 'copy')
    & "$PROMPT_DIR\run-prompt.ps1" -PromptType note -Action $Action
}

function prompt-product {
    <#
    .SYNOPSIS
        商品設計プロンプトを実行
    .PARAMETER Action
        show, copy, open のいずれか（デフォルト: copy）
    #>
    param([string]$Action = 'copy')
    & "$PROMPT_DIR\run-prompt.ps1" -PromptType product -Action $Action
}

function prompt-video {
    <#
    .SYNOPSIS
        AI動画収益化プロンプトを実行
    .PARAMETER Action
        show, copy, open のいずれか（デフォルト: copy）
    #>
    param([string]$Action = 'copy')
    & "$PROMPT_DIR\run-prompt.ps1" -PromptType video -Action $Action
}

function prompt-list {
    <#
    .SYNOPSIS
        利用可能なプロンプト一覧を表示
    #>
    & "$PROMPT_DIR\run-prompt.ps1" -PromptType all
}

# エクスポート
Export-ModuleMember -Function prompt-note, prompt-product, prompt-video, prompt-list

# 使い方をコンソールに表示
Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "📚 Note Articles Prompt Aliases" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Cyan

Write-Host "利用可能なコマンド:" -ForegroundColor White
Write-Host ""
Write-Host "  prompt-note      " -NoNewline -ForegroundColor Green
Write-Host "記事構成設計プロンプト（クリップボードにコピー）" -ForegroundColor Gray
Write-Host "  prompt-product   " -NoNewline -ForegroundColor Green
Write-Host "商品設計プロンプト（クリップボードにコピー）" -ForegroundColor Gray
Write-Host "  prompt-video     " -NoNewline -ForegroundColor Green
Write-Host "AI動画収益化プロンプト（クリップボードにコピー）" -ForegroundColor Gray
Write-Host "  prompt-list      " -NoNewline -ForegroundColor Green
Write-Host "すべてのプロンプト一覧を表示" -ForegroundColor Gray
Write-Host ""
Write-Host "オプション:" -ForegroundColor White
Write-Host "  -Action show     " -NoNewline -ForegroundColor Yellow
Write-Host "内容を表示" -ForegroundColor Gray
Write-Host "  -Action copy     " -NoNewline -ForegroundColor Yellow
Write-Host "クリップボードにコピー（デフォルト）" -ForegroundColor Gray
Write-Host "  -Action open     " -NoNewline -ForegroundColor Yellow
Write-Host "エディタで開く" -ForegroundColor Gray
Write-Host ""
Write-Host "使用例:" -ForegroundColor White
Write-Host "  prompt-note              " -NoNewline -ForegroundColor Cyan
Write-Host "# 記事プロンプトをコピー" -ForegroundColor Gray
Write-Host "  prompt-product -Action show  " -NoNewline -ForegroundColor Cyan
Write-Host "# 商品プロンプトを表示" -ForegroundColor Gray
Write-Host "  prompt-video -Action open    " -NoNewline -ForegroundColor Cyan
Write-Host "# 動画プロンプトをエディタで開く" -ForegroundColor Gray
Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Cyan
