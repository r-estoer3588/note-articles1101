
$TaskName = "SNS_Analysis_Nightly_Update"
$Time = "22:00"
$ScriptPath = "C:\Repos\note-articles\tools\sns_integrated_analyzer.py"
$WorkDir = "C:\Repos\note-articles"

# アクションの定義: PowerShellを開いてツールを実行
# -NoExit をつけることで、実行後もウィンドウが閉じずに結果を確認できる
$Action = New-ScheduledTaskAction -Execute "pwsh.exe" -Argument "-ExecutionPolicy Bypass -NoExit -Command ""Set-Location '$WorkDir'; python '$ScriptPath' --update-manual"""

# トリガーの定義: 毎日 22:00
$Trigger = New-ScheduledTaskTrigger -Daily -At $Time

# 設定の定義: 電源接続時のみなどの制限を解除
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

# タスクの登録
Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Description "SNS統合分析ツールの手動更新を毎日夜に起動" -Force

Write-Host "タスク '$TaskName' を登録しました。毎日 $Time に起動します。" -ForegroundColor Green
Write-Host "テスト実行するには以下のコマンドを入力してください:"
Write-Host "Start-ScheduledTask -TaskName '$TaskName'" -ForegroundColor Yellow
