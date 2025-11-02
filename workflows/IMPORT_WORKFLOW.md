# n8n ワークフロー インポート手順

## 🎯 改善版ワークフローをインポート

### 理由
- ✅ Notion 認証エラーの根本対策
- ✅ Docker の localFileTrigger の代わりに Cron ベースのファイル監視を実装
- ✅ 手動テスト機能を統合（即座に動作確認可能）
- ✅ OpenAI API 呼び出しを環境変数経由で安全に実装

### インポート手順

1. **n8n UI を開く**
   - http://localhost:5678

2. **画面右上 "Projects" → "Workflows"**

3. **左上 "+" → "Import from file"**

4. **ファイル選択**
   ```
   c:\Repos\note-articles\workflows\notes-to-notion-improved.json
   ```

5. **インポート完了後**
   - ワークフロー名: "Notes to Notion Auto Organizer (Improved)"
   - 左側パネルで確認可能

---

## 🔧 初期設定（重要）

### 1. Notion 認証情報を新規作成

1. 左下アイコン → **Credentials**
2. "+ Create New Credential"
3. **Type**: Notion API
4. **Name**: `Notion account`
5. **Notion Internal Integration Token**: 
   - https://www.notion.so/my-integrations にアクセス
   - 新規インテグレーション作成
   - トークンをコピー

6. **Test** ボタンで接続確認

### 2. ワークフロー内で認証情報を紐付け

1. ワークフロー開く
2. 「Notion Create Item」ノードをクリック
3. 右パネル → **Authentication** セクション
4. Dropdown から「Notion account」を選択
5. 「Notion Create Item (Test)」も同様に設定

### 3. 環境変数を設定

```powershell
# .env ファイル作成
@"
OPENAI_API_KEY=sk-proj-YOUR_API_KEY_HERE
"@ | Out-File -Encoding UTF8 c:\Repos\note-articles\workflows\.env
```

コンテナ再起動：
```powershell
cd c:\Repos\note-articles\workflows
docker-compose down
docker-compose up -d
```

---

## 🧪 手動テストで検証

### テストフロー（下部）を実行

1. **"Manual Test Trigger" ノードを右クリック**
2. **"Execute node"**

### 期待される結果

1. テストデータが生成される
2. Mock AI Response で category/tags が設定される
3. Format for Notion (Test) でデータ整形
4. **Notion Create Item (Test) で DB に新規ページ作成**

### Notion 側で確認

Database を開く → 新規ページ「test_note」が追加されているはず
- Category: 技術メモ
- Tags: Python, 機械学習, データ分析
- Content: テストテキスト

---

## 🚀 本格運用開始

### Cron ベースのファイル監視を有効化

1. **「Scan Notes Folder (Every 5 min)」トリガーを有効化**
   - スケジュール: 5分ごと
   - `/notes` フォルダをスキャン
   - 新しいファイルのみ処理

2. **C:\Notes に新規テキストファイルを作成**

3. **5分以内にワークフロー実行**
   - OpenAI で category/tags を自動生成
   - Notion DB に自動追加

---

## ⚙️ ワークフロー構成図

```
┌─────────────────────────────────────────────────────────────────┐
│  【自動フロー】                                                  │
│  Scan Notes Folder (5分毎)                                       │
│         ↓                                                        │
│  Find New Files (find コマンド)                                  │
│         ↓                                                        │
│  Parse File Path (ファイルパス抽出)                              │
│         ↓                                                        │
│  Read Note File (ファイル読み込み)                               │
│         ↓                                                        │
│  Set Note Metadata (メタデータ設定)                              │
│         ↓                                                        │
│  OpenAI Category Tagging (API 呼び出し)                          │
│         ↓                                                        │
│  Format for Notion (Notion形式に整形)                            │
│         ↓                                                        │
│  Notion Create Item (DB に保存) ✅                               │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  【テストフロー】                                                │
│  Manual Test Trigger (手動実行)                                 │
│         ↓                                                        │
│  Manual Test Data (ダミーデータ入力)                             │
│         ↓                                                        │
│  Mock AI Response (テスト用モック)                               │
│         ↓                                                        │
│  Format for Notion (Test)                                       │
│         ↓                                                        │
│  Notion Create Item (Test) ✅                                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🐛 トラブル対応

### ❌ 認証エラー継続

```powershell
# コンテナの永続ボリュームをクリア
docker volume rm n8n_data

# コンテナ再起動
docker-compose down
docker-compose up -d
```

### ❌ ファイル読み込み失敗

```bash
# コンテナ内で確認
docker exec n8n-notes-organizer ls -la /notes
```

### ❌ OpenAI API エラー

- `.env` ファイルの API Key を確認
- Docker ログ確認: `docker logs n8n-notes-organizer`

---

## 📞 参考リソース

- n8n Notion ノード: https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.notion/
- Notion API: https://developers.notion.com/
- OpenAI API: https://platform.openai.com/docs/api-reference
