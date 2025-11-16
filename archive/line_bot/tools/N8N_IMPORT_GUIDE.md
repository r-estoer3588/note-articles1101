# n8nワークフローインポートガイド

## 前提条件

1. **n8nが起動していること**
   - デフォルトURL: http://localhost:5678
   - Docker環境の場合は `http://host.docker.internal:5679` でFlask APIにアクセス可能であること

2. **Flask APIが稼働していること**
   ```powershell
   # Flask API起動確認
   netstat -ano | findstr :5679
   # → LISTENING が表示されればOK
   
   # ヘルスチェック
   curl.exe http://localhost:5679/health
   # → {"status":"ok"} が返ればOK
   ```

## インポート手順

### 1. n8nにログイン

ブラウザで http://localhost:5678 を開く

### 2. ワークフローをインポート

1. **左サイドバー** から「**Workflows**」をクリック
2. 右上の「**Import from File**」または「**Import**」ボタンをクリック
3. ファイル選択で `c:\Repos\note-articles\tools\n8n_workflow_menu_sqlite.json` を選択
4. インポート完了後、ワークフローが開く

### 3. Webhook URLを確認・設定

1. ワークフロー内の「**LINE Webhook**」ノードをクリック
2. **Webhook URLs** セクションに表示されるURLをコピー
   - 例: `https://n8n.yourdomain.com/webhook/line-menu` または `http://localhost:5678/webhook-test/line-menu`
3. このURLをLINE Developers ConsoleのWebhook URLに設定（後述）

### 4. Flask API接続確認

1. 「**ユーザー状態取得**」ノードをクリック
2. URL欄を確認:
   ```
   http://host.docker.internal:5679/api/state/={{ $json.userId }}
   ```
   - **Docker環境**: `host.docker.internal:5679` (デフォルト)
   - **ローカル環境**: `localhost:5679` に変更

3. 「**状態を更新**」ノードも同様に確認

### 5. ワークフローを保存・有効化

1. 右上の「**Save**」ボタンをクリック
2. 右上のトグルスイッチを「**Active**」に切り替え

## LINE Developersコンソール設定

### Webhook URL設定

1. [LINE Developers Console](https://developers.line.biz/console/) にログイン
2. 対象のチャネルを選択
3. 「**Messaging API**」タブを開く
4. 「**Webhook settings**」セクション:
   - **Webhook URL**: n8nのWebhook URLを入力
   - **Use webhook**: ON に設定
   - **Verify** ボタンでテスト（成功すればOK）

### リプライメッセージ設定

「**Messaging API**」タブ内:
- **Allow bot to join group chats**: ON（グループ対応する場合）
- **Auto-reply messages**: OFF（n8nで制御するため）
- **Greeting messages**: OFF（任意）

## テスト手順

### 1. Flask API動作確認

```powershell
# 新規ユーザー作成
$body = @{state='idle'} | ConvertTo-Json
Invoke-RestMethod -Uri 'http://localhost:5679/api/state/test_user_999' -Method Post -Body $body -ContentType 'application/json'

# 状態取得
curl.exe http://localhost:5679/api/state/test_user_999
```

### 2. LINE Botテスト

LINEアプリで以下のメッセージを送信:

1. **ヘルプ表示**: `menu:help` または `c`
2. **投稿生成開始**: `menu:generate` または `a`
3. **件数入力**: `5`
4. **テーマ入力**: `副業で月5万円稼ぐ方法`
5. **投稿ナビゲーション**: クイックリプライの「次へ」「前へ」ボタン
6. **破棄テスト**: クイックリプライの「破棄」ボタン

### 3. ログ確認

#### Flask APIログ
```powershell
# Flaskサーバーを起動したターミナルで確認
# GET/POSTリクエストのログが表示される
```

#### n8nログ
1. n8nワークフローのExecutionsタブを開く
2. 各実行をクリックして詳細を確認
3. エラーがあれば赤く表示される

## トラブルシューティング

### Flask APIに接続できない

**症状**: n8nから `ECONNREFUSED` エラー

**原因**: Docker環境でホストのFlask APIに到達できない

**解決策**:
```powershell
# Windows: Docker Desktopの設定確認
# Settings → Resources → Network → "Allow privileged port access"をON

# または、n8nをDocker外で起動
npm install -g n8n
n8n start
```

### Webhook URLが無効

**症状**: LINE Developers ConsoleでVerifyが失敗

**原因**: 
- n8nワークフローが非アクティブ
- ngrokなどの外部トンネルが必要（ローカル環境の場合）

**解決策**:
```powershell
# ngrokでトンネル作成
ngrok http 5678

# ngrokが表示するURLをLINE Webhook URLに設定
# 例: https://abc123.ngrok.io/webhook/line-menu
```

### 投稿が生成されない

**症状**: `hogey_algorithm.py` が実行されない

**原因**: Pythonパスまたは依存関係の問題

**解決策**:
```powershell
# hogey_algorithm.pyの動作確認
cd c:\Repos\note-articles\tools
python hogey_algorithm.py --json --count 3 --theme "テスト" --type buzz

# 依存関係確認
pip list | Select-String openai
```

### 状態がリセットされない

**症状**: `current_index` が0に戻らない

**原因**: 修正前の `line_bot_state_manager.py` が稼働中

**解決策**:
```powershell
# Flaskサーバー再起動
Get-Process python | Where-Object { $_.MainWindowTitle -like '*line_bot_api*' } | Stop-Process -Force
cd c:\Repos\note-articles\tools
python line_bot_api.py
```

## 成功の判断基準

✅ **全て正常に動作している状態**:
1. Flask API `/health` が200 OK
2. n8nワークフローがActive状態
3. LINE BotでメッセージをDEBUG: LINE webhook receivedbotに送信すると、n8n Executionsに実行ログが表示される
4. 投稿生成後、クイックリプライボタンで「次へ」「前へ」が機能する
5. 「破棄」ボタンで `current_index` が0にリセットされる

## 次のステップ

インポート・テスト完了後:
1. ✅ エンドツーエンドテスト（破棄→再生成フロー）
2. 📊 本番環境デプロイ（n8n CloudまたはVPS）
3. 🔐 環境変数の設定（OpenAI API Key、LINE Channel Secret）

---

**作成日**: 2025-11-16  
**対象ファイル**: `n8n_workflow_menu_sqlite.json`  
**関連ファイル**: `line_bot_api.py`, `line_bot_state_manager.py`, `hogey_algorithm.py`
