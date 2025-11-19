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

# げすいぬ化記事改善ツールのエイリアス
function Start-GesuinuTool {
    Push-Location C:\Repos\note-articles
    try {
        .\gesuinu.ps1 @args
    } finally {
        Pop-Location
    }
}

# 錬金王スタイル記事リライトツールのエイリアス
function Start-RenkinTool {
    Push-Location C:\Repos\note-articles
    try {
        .\renkin.ps1 @args
    } finally {
        Pop-Location
    }
}

# エイリアス設定
Set-Alias education Start-EducationTool
Set-Alias edu Start-EducationTool
Set-Alias gesuinu Start-GesuinuTool
Set-Alias gn Start-GesuinuTool
Set-Alias renkin Start-RenkinTool
Set-Alias rk Start-RenkinTool

# 使い方:
# どのディレクトリからでも以下のコマンドで起動:
#   education / edu      # 教育カテゴリ別投稿生成
#   gesuinu / gn         # げすいぬ化記事改善
#   renkin / rk          # 錬金王スタイル記事リライト
#
# 例:
#   education -Help
#   education -Setup
#   gesuinu -Help
#   gesuinu -Show
#   gesuinu -File "articles/sample.md"
#   renkin -Help
#   renkin -Template
#   renkin -Examples
#   renkin "articles/my-article.md"
