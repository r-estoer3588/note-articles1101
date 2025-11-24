# ⚡ PowerShell から「どこでも起動」セットアップガイド

このガイドに従うと、PowerShell で **`dashboard`** と入力するだけでモニタリングダッシュボードを起動できるようになります。

---

## 🎯 完成イメージ

セットアップ後、PowerShell で以下のように使えます：

```powershell
# ダッシュボード起動
dashboard

# または
Start-BufferDashboard

# 停止
Stop-BufferDashboard
```

---

## 📋 セットアップ手順

### ステップ 1: PowerShell プロファイルの場所を確認

PowerShell を開いて、以下のコマンドを実行：

```powershell
$PROFILE
```

表示されたパスをメモしてください（例: `C:\Users\YourName\Documents\PowerShell\Microsoft.PowerShell_profile.ps1`）

---

### ステップ 2: プロファイルファイルを開く（または作成）

```powershell
# プロファイルが存在しなければ作成
if (!(Test-Path $PROFILE)) {
    New-Item -Path $PROFILE -ItemType File -Force
}

# メモ帳でプロファイルを開く
notepad $PROFILE
```

---

### ステップ 3: プロファイルに以下を追加

メモ帳が開いたら、**一番下に**以下の内容を貼り付けてください：

```powershell
# Buffer Monitoring Dashboard
. "c:\Repos\note-articles\tools\monitoring\start-dashboard.ps1"
```

> **⚠️ 重要**: パスが異なる場合は、実際の `start-dashboard.ps1` のパスに変更してください。

保存して、メモ帳を閉じます。

---

### ステップ 4: PowerShell を再起動

PowerShell ウィンドウを閉じて、もう一度開きます。

---

### ステップ 5: 動作確認

```powershell
dashboard
```

と入力して Enter を押すと、自動的に：

1. サーバーが起動
2. ブラウザが開く
3. ダッシュボードが表示される

---

## 🛠️ 使い方

### ダッシュボードを起動

```powershell
dashboard
```

または

```powershell
Start-BufferDashboard
```

### ダッシュボードを停止

```powershell
Stop-BufferDashboard
```

### パスを指定して起動（デフォルト以外の場所にある場合）

```powershell
Start-BufferDashboard -Path "D:\Projects\my-monitoring"
```

---

## 🔧 トラブルシューティング

### 問題: `dashboard` と入力してもコマンドが見つからない

**原因**: PowerShell プロファイルが正しく読み込まれていない

**解決策**:

1. PowerShell を再起動
2. または、手動で読み込む：
   ```powershell
   . $PROFILE
   ```

---

### 問題: 「スクリプトの実行がシステムで無効になっている」エラー

**原因**: PowerShell の実行ポリシーが制限されている

**解決策**:
PowerShell を**管理者として実行**し、以下を実行：

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

確認を求められたら `Y` を入力して Enter。

その後、通常の PowerShell ウィンドウで再度試してください。

---

### 問題: パスが見つからない

**原因**: `start-dashboard.ps1` の場所が違う

**解決策**:

1. エクスプローラーで `start-dashboard.ps1` を探す
2. ファイルを右クリック → 「パスのコピー」
3. `$PROFILE` を開き、コピーしたパスに修正
4. PowerShell を再起動

---

## 🎨 カスタマイズ

### デフォルトパスを変更

`start-dashboard.ps1` を開いて、9 行目を編集：

```powershell
[string]$Path = "c:\Repos\note-articles\tools\monitoring"
```

↓ 自分の環境に合わせて変更

```powershell
[string]$Path = "D:\MyProjects\monitoring"
```

---

### エイリアス（短縮名）を変更

`start-dashboard.ps1` の最後の方（77 行目あたり）を編集：

```powershell
Set-Alias -Name dashboard -Value Start-BufferDashboard
```

↓ 好きな名前に変更（例: `mon`, `d`, `buf` など）

```powershell
Set-Alias -Name mon -Value Start-BufferDashboard
```

---

## 📚 その他の便利コマンド

### 現在実行中のジョブを確認

```powershell
Get-Job
```

### すべてのジョブを停止

```powershell
Get-Job | Stop-Job
Get-Job | Remove-Job
```

---

## ✅ 完了！

これで、どのディレクトリからでも `dashboard` と入力するだけでモニタリングダッシュボードを起動できます。

毎日のデータ記録がさらに簡単になりました！🎉
