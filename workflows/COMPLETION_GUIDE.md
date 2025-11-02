# n8n Notes to Notion Auto Organizer - 完成ガイド

## 🎯 現状分析

### 主な問題
1. ❌ **Notion 認証エラー**: `Node does not have any credentials set for 'notionApi'`
2. ❌ **ファイル監視未動作**: Docker 環境の `localFileTrigger` が検知していない
3. ❌ **フローが Notion まで到達していない**: 手動テストでも途中で停止

### 成功している点
✅ ファイルマウント: `/notes` にホストファイルが同期されている  
✅ 認証情報登録: UI 上では「Notion account」が表示されている  
✅ OpenAI API キー: 環境変数経由で利用可能

---

## 🔧 段階的解決手順

### **ステップ 1: Docker 環境の再構築**

```powershell
# 1. コンテナ停止・削除
docker-compose -f c:\Repos\note-articles\workflows\docker-compose.yml down

# 2. ボリューム削除（認証情報も削除される）
docker volume rm n8n_data

# 3. 環境変数ファイル作成（OpenAI API キー設定用）
@"
OPENAI_API_KEY=sk-proj-YOUR_KEY_HERE
"@ | Out-File -Encoding UTF8 c:\Repos\note-articles\workflows\.env

# ⚠️ YOUR_KEY_HERE を実際のキーに置き換える
```

### **ステップ 2: n8n 再起動**

```powershell
cd c:\Repos\note-articles\workflows

# Docker Compose で起動（環境変数自動読み込み）
docker-compose up -d

# ログを確認
docker logs n8n-notes-organizer -f
```

### **ステップ 3: Notion 認証の再設定**

1. **ブラウザで n8n UI にアクセス**
   - URL: `http://localhost:5678`
   - ユーザー: `admin`
   - パスワード: `change_this_password_123`

2. **左下の設定アイコン → Credentials**

3. **「Notion account」削除（古い設定を消す）**
   - 右上の三点メニュー → Delete

4. **新規作成**
   - "+ Create New" ボタン
   - Type: **Notion API**
   - Internal ID: `notionApi` (必須)
   - Authentication: **Notion API**
   - API Token: `ntn_YOUR_TOKEN_HERE`
   - 💡 Notion から取得方法:
     - https://developers.notion.com/ にアクセス
     - マイ インテグレーション → 新規作成
     - Internal Name: "n8n-notes-organizer"
     - Capability 有効化: "Read", "Update", "Insert"
     - Token をコピー

5. **Test Connection で動作確認**

### **ステップ 4: ワークフロー内の認証情報を再紐付け**

1. **ワークフロー開く**: "Notes to Notion Auto Organizer"

2. **「Notion Create Item」ノードをクリック**

3. **右パネルの "Authentication" セクション**
   - Dropdown から **「Notion account」** を選択
   - 保存

4. **「Notion Create Item (Test)」ノードも同様に設定**

### **ステップ 5: 手動テストで確認**

1. **ワークフロー左上から「Manual Test Trigger」を検索**

2. **該当ノード右上の ▶️ アイコンをクリック**

3. **「Execute node」が実行される**

4. **期待される動き**
   - Manual Test Data ノード → テストデータを生成
   - Mock AI Response ノード → ダミーの category/tags を返す
   - Format for Notion (Test) ノード → Notion 用フォーマット
   - Notion Create Item (Test) → **Notion DB に新規ページ作成**

5. **Notion 側で確認**
   - 該当 Database を開く
   - タイトル「test_note」の新規ページが追加されているか確認
   - Category: 技術メモ
   - Tags: Python, 機械学習, データ分析
   - Content: テストテキスト

---

## 🚀 本格運用設定

### **Cron ベースのファイル監視設定**

元のワークフロー JSON の「Watch Notes Folder」を無効化し、以下に変更：

```javascript
{
  "parameters": {
    "rule": {
      "interval": [
        {
          "field": "minutes",
          "value": 5  // 5分ごとにスキャン
        }
      ]
    }
  },
  "id": "schedule-trigger",
  "name": "Scan Notes Folder (Every 5 min)",
  "type": "n8n-nodes-base.scheduleTrigger",
  "typeVersion": 1.2
}
```

### **新ファイルを検知するコマンド**

```bash
find /notes -type f \( -name "*.txt" -o -name "*.md" \) -newer /tmp/last_scan
```

- `/tmp/last_scan` の timestamp より新しいファイルを検出
- スキャン完了後、タッチしてタイムスタンプを更新

---

## 🐛 よくあるエラーと対処

| エラー | 原因 | 対処 |
|--------|------|------|
| `Node does not have credentials` | 認証情報が紐付いていない | ステップ 4 を実行 |
| `Unauthorized (401)` | Notion API Token 間違い | Token を再確認・再生成 |
| `File not found: /notes/...` | マウント設定エラー | `docker-compose.yml` の Volume を確認 |
| `OpenAI API Error` | API Key 未設定/無効 | `.env` ファイルの OPENAI_API_KEY を確認 |
| `Empty file content` | バイナリ読み込みエラー | `readBinaryFile` の encoding を UTF-8 に確認 |

---

## 📋 Notion DB プロパティ要件

必ず以下の Property を DB に作成してください：

| Property Name | Type | 説明 |
|---------------|------|------|
| Title | Title | ページタイトル（必須） |
| Content | Rich Text | ノート内容 |
| Category | Text | OpenAI が生成 |
| Tags | Multi-select | タグ複数選択 |
| Processed | Checkbox | 処理完了フラグ |

---

## ✅ チェックリスト

- [ ] `docker-compose.yml` で C:/Notes → /notes マウント確認
- [ ] `.env` ファイルに OPENAI_API_KEY 設定
- [ ] Docker コンテナ再起動
- [ ] n8n UI で Notion 認証情報が "notionApi" ID で登録
- [ ] ワークフローの「Notion Create Item」と「Notion Create Item (Test)」に認証情報を紐付け
- [ ] 手動テストで Notion に新規ページが作成されることを確認
- [ ] スケジュール Trigger を有効化
- [ ] C:\Notes に新規テキストファイルを作成して動作確認

---

## 🆘 さらにサポートが必要な場合

実行ログを確認：
```powershell
docker logs n8n-notes-organizer --follow
```

n8n UI の "Executions" タブで失敗原因を確認。
