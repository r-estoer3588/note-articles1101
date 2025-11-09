# LINE Bot 引き継ぎドキュメント

## 🎯 目標
ホゲーアルゴリズム（X投稿自動生成）をLINE Botでスマホから操作できるようにする。
ボタンをポチポチするだけでコマンド不要。

## ✅ 完了した作業

### 1. SQLite状態管理の実装
- ✅ `line_bot_states.db` 作成済み
- ✅ `line_bot_state_manager.py` 作成・動作確認済み
- ✅ テーブル構造: `user_id, state, count, theme, posts_data, current_index, updated_at, type`

### 2. n8nワークフロー
- ✅ `n8n_workflow_menu_sqlite.json` 作成済み（SQLite版）
- ✅ Google Sheets依存を削除してSQLiteに置き換え
- ✅ Channel Access Token設定済み
- ✅ Webhook URL: `/webhook/line-menu`（Webhookノードのパス設定は `line-menu`）

### 3. LINE設定
- ✅ LINE Official Account作成済み（@675dzjuv）
- ✅ Messaging API有効化
- ✅ Channel Access Token発行済み: `wC3gxIxXv1YSwIcHr9gSY30+xp8pmF8uPbCsAcNpAnOqI5e6m4VdBI3Dc4/tSg1DOjQdFxYV0285aXsK3mN/Oim0eJuQmnJbD28azHAhfBrxEFosh9kdykEMm9rbeMOpiMCKsQnP2Cg2g8S7girINwdB04t89/1O/w1cDnyilFU=`
- ✅ チャット: ON
- ✅ あいさつメッセージ: OFF
- ✅ Webhook: ON

### 4. インフラ
- ✅ n8n: Dockerで起動中（localhost:5678）
- ✅ localtunnel: 実行中（`https://yummy-onions-slide.loca.lt`）

## ❌ 未完了・現在の問題

### 問題: Webhookが404を返す
**エラーメッセージ:**
```
{"code":404,"message":"The requested webhook \"POST line-menu\" is not registered."}
```

**原因:**
LINE DevelopersのWebhook URLが`/line-menu`のままのため、n8nのエンドポイント`/webhook/line-menu`に到達していない。

## 🔧 次にやること

### ステップ1: n8nワークフローをActive化
1. n8n画面を開く: `http://localhost:5678`
2. ワークフロー「ホゲーアルゴリズム LINE Bot メニュー版 (SQLite)」を開く
3. 右上の「**Inactive**」スイッチをクリックして「**Active**」（緑色）に変更
4. 「Save」ボタンをクリック

### ステップ2: LINE Webhook URL設定
1. LINE Developers Console: https://developers.line.biz/console/
2. Messaging API設定タブ
3. Webhook URL: `https://yummy-onions-slide.loca.lt/webhook/line-menu`
4. 「検証」ボタンをクリック → 成功を確認

### ステップ3: 動作テスト
1. スマホでLINE公式アカウント（@675dzjuv）を友だち追加
2. `menu:help` と送信
3. n8nの「Executions」タブで実行ログを確認

## 📁 重要ファイル

### Python
- `c:\Repos\note-articles\tools\line_bot_state_manager.py` - SQLite状態管理
- `c:\Repos\note-articles\tools\hogey_algorithm.py` - 投稿生成エンジン
- `c:\Repos\note-articles\tools\line_bot_helper.py` - LINEメッセージフォーマット

### n8n
- `c:\Repos\note-articles\tools\n8n_workflow_menu_sqlite.json` - 最新ワークフロー（SQLite版）
- ~~`n8n_workflow_menu_complete.json`~~ - 削除済み（Google Sheets版・旧）

### データベース
- `c:\Repos\note-articles\tools\line_bot_states.db` - SQLiteデータベース

## 🔑 認証情報

### LINE
- Channel ID: 既にDevelopers Consoleで確認可能
- Channel Secret: 既にDevelopers Consoleで確認可能
- Channel Access Token: `wC3gxIxXv1YSwIcHr9gSY30+...（上記参照）`

### n8n
- URL: http://localhost:5678
- Docker起動コマンド: `docker ps` で確認可能

### localtunnel
- 現在のURL: `https://yummy-onions-slide.loca.lt`
- 再起動コマンド: `npx -y localtunnel --port 5678`

## 🐛 トラブルシューティング

### Webhook 503エラー
- **原因:** n8nが起動していない or ワークフローがInactive
- **対処:** Dockerとワークフローの状態を確認

### Webhook 404エラー
- **原因:** Webhook URLのパスが`/webhook/line-menu`になっていない
- **対処:** LINE DevelopersのWebhook設定を修正

### localtunnel接続エラー
- **対処:** ターミナルで再実行: `npx -y localtunnel --port 5678`

## 📋 テストコマンド

### SQLite状態管理テスト
```powershell
cd C:\Repos\note-articles\tools
python line_bot_state_manager.py
```

### Webhookローカルテスト
```powershell
curl -X POST http://localhost:5678/webhook/line-menu -H "Content-Type: application/json" -d '{\"events\":[{\"type\":\"message\",\"replyToken\":\"test\",\"source\":{\"userId\":\"test123\"},\"message\":{\"type\":\"text\",\"text\":\"menu:help\"}}]}'
```

## 📝 ワークフロー仕様

### コマンド
- `menu:help` - ヘルプ表示
- `menu:generate` - バズ投稿生成（件数選択→テーマ選択）
- `menu:today` - 今日のテーマで生成（曜日ごとのカテゴリ）
- `menu:trilogy` - 3部作ストーリー生成

### フロー
1. Webhook受信 → コマンド解析
2. SQLiteから状態取得
3. 状態判定（件数選択/テーマ選択/生成実行/ヘルプ）
4. Python実行（投稿生成）
5. SQLiteに状態更新
6. LINE返信

### 状態遷移
- `idle` → `selecting_count` → `selecting_theme` → `generating` → `viewing_posts` → `idle`

## 🚀 最終チェックリスト

- [ ] n8nワークフローをActive化
- [ ] LINE Webhook URL設定＆検証成功
- [ ] スマホからメッセージ送信テスト
- [ ] n8n Executionsタブでログ確認
- [ ] 投稿生成の動作確認
- [ ] リッチメニュー有効化（オプション）

## 💡 今後の拡張

1. リッチメニューボタンの実装
2. 投稿のX自動投稿機能
3. 学習機能の追加
4. ユーザーごとの統計表示

---

**最終更新:** 2025年11月9日  
**作成者:** GitHub Copilot  
**ステータス:** n8n Active化待ち
