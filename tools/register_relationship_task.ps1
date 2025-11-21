# Register Task Scheduler for Relationship Auto Poster
$TaskName = "NoteArticles_Relationship_AutoPost"
$ScriptPath = Join-Path (Get-Location) "tools\run_relationship_auto_post.ps1"
$PythonPath = (Get-Command python).Source

# Create the action
$Action = New-ScheduledTaskAction -Execute "pwsh.exe" -Argument "-ExecutionPolicy Bypass -File `"$ScriptPath`""

# Create the trigger (Every 1 hour)
$Trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).Date.AddHours(7) -RepetitionInterval (New-TimeSpan -Hours 1) -RepetitionDuration (New-TimeSpan -Days 3650)

# Create the settings
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

# Register the task
Register-ScheduledTask -Action $Action -Trigger $Trigger -Settings $Settings -TaskName $TaskName -Description "Auto-posts to Threads for Relationship Account" -Force

Write-Host "Task '$TaskName' registered successfully."
