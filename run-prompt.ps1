#!/usr/bin/env pwsh
<#
.SYNOPSIS
    プロンプトランナーのラッパースクリプト（note-articles用）

.DESCRIPTION
    note-articlesディレクトリから実行できるように、prompt/run-prompt.ps1を呼び出します
#>

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet('note', 'product', 'video', 'all')]
    [string]$PromptType = 'all',
    
    [Parameter(Mandatory=$false)]
    [ValidateSet('show', 'copy', 'open')]
    [string]$Action = 'copy',
    
    [Parameter(Mandatory=$false)]
    [string]$Section = ''
)

# 実際のスクリプトのパス
$ActualScript = Join-Path $PSScriptRoot "prompt\run-prompt.ps1"

if (-not (Test-Path $ActualScript)) {
    Write-Host "❌ エラー: スクリプトが見つかりません" -ForegroundColor Red
    Write-Host "   期待パス: $ActualScript" -ForegroundColor Yellow
    exit 1
}

# 実際のスクリプトを実行
if ($Section) {
    & $ActualScript -PromptType $PromptType -Action $Action -Section $Section
} else {
    & $ActualScript -PromptType $PromptType -Action $Action
}
