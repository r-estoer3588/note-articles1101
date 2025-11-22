#!/usr/bin/env pwsh
<#
.SYNOPSIS
    投稿リライトツールのラッパー

.DESCRIPTION
    指定されたCSVファイル、またはフォルダ内の全CSVファイルを
    「レス卒先輩」ペルソナに合わせてリライトします。

.EXAMPLE
    .\tools\refine_posts.ps1 -File tools/outputs/buffer_split/Week1_Day1.csv
    単一ファイルをリライト

.EXAMPLE
    .\tools\refine_posts.ps1 -All
    tools/outputs/buffer_split/ 内の全ファイルをリライト（確認あり）
#>

param(
    [string]$File,
    [switch]$All
)

$ScriptPath = Join-Path $PSScriptRoot "rewrite_csv_with_persona.py"
$TargetDir = Join-Path $PSScriptRoot "outputs\buffer_split"

if ($File) {
    # 単一ファイル処理
    if (-not (Test-Path $File)) {
        Write-Error "ファイルが見つかりません: $File"
        exit 1
    }
    python $ScriptPath $File
}
elseif ($All) {
    # 全ファイル処理
    $files = Get-ChildItem $TargetDir -Filter "Week*_Day*.csv" | Where-Object { $_.Name -notlike "*_refined.csv" }
    
    Write-Host "以下のファイルを処理します:" -ForegroundColor Cyan
    $files | ForEach-Object { Write-Host "  - $($_.Name)" }
    
    $confirm = Read-Host "実行しますか？ (y/n)"
    if ($confirm -ne "y") { exit }
    
    foreach ($f in $files) {
        Write-Host "処理中: $($f.Name)" -ForegroundColor Yellow
        python $ScriptPath $f.FullName
    }
}
else {
    Write-Host "使用法:"
    Write-Host "  .\tools\refine_posts.ps1 -File <path>"
    Write-Host "  .\tools\refine_posts.ps1 -All"
}
