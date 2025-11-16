# PowerShell プロファイル用設定
# このファイルの内容を PowerShell プロファイルに追加してください

# 教育カテゴリ別投稿生成ツールのエイリアス
function Start-EducationTool {
    Push-Location C:\Repos\note-articles
    try {
        .\education.ps1 @args
    } finally {
        Pop-Location
    }
}

# エイリアス設定
Set-Alias education Start-EducationTool
Set-Alias edu Start-EducationTool

# 使い方:
# どのディレクトリからでも以下のコマンドで起動:
#   education
#   edu
#   education -Help
#   education -Setup
