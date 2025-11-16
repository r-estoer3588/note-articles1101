# =====================================================
# SNSマネタイズプラン生成ツール
# =====================================================

function Start-MonetizePlanner {
    <#
    .SYNOPSIS
        SNSマネタイズプラン生成ツールを起動
    
    .DESCRIPTION
        対話型でSTEP1質問に回答し、
        あなたの人生を変える本気のマネタイズプランを設計します
        
        STEP1: 現状の深掘り分析（5カテゴリ、20以上の質問）
        STEP2: 包括的なマネタイズプラン生成
    
    .EXAMPLE
        monetize
        対話型でSTEP1質問に回答
    
    .EXAMPLE
        monetize -Api
        OpenAI APIで自動プラン生成
    
    .EXAMPLE
        monetize -PromptOnly
        プロンプトのみ生成してクリップボードにコピー
    
    .EXAMPLE
        monetize -Help
        詳細ヘルプを表示
    #>
    
    Push-Location "C:\Repos\note-articles"
    try {
        & .\monetize.ps1 @args
    }
    finally {
        Pop-Location
    }
}

Set-Alias monetize Start-MonetizePlanner
Set-Alias mz Start-MonetizePlanner

Write-Host "💰 マネタイズ: " -ForegroundColor Yellow -NoNewline
Write-Host "monetize" -ForegroundColor Cyan -NoNewline
Write-Host " または " -ForegroundColor Gray -NoNewline
Write-Host "mz" -ForegroundColor Cyan
