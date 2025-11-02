# 🚨 トラブルシューティング - ノードエラーの対処法

## 現在のエラー状況

スクリーンショットから以下のノードでエラーが発生している可能性:

1. ❓ **Watch Notes Folder** - n8n-nodes-fs の問題
2. ❓ **Read Note File** - n8n-nodes-fs の問題
3. ❓ **Delete Old File** - n8n-nodes-fs の問題
4. ⚠️ **Get All Notes from Notion** - Notion API の問題

---

## 🔧 解決策1: 簡易版を使う(推奨)

**n8n-nodes-fs を使わない**シンプル版を作成しました。

### 使い方

1. **新しいワークフローをインポート**
   - `notes-to-notion-simple.json` を n8n にインポート

2. **手動トリガーでテスト**
   - 「Start」ノードをクリック
   - 「Execute Node」でテスト実行

3. **Set Test Data ノードでテストデータを設定**
   ```
   fileName: test-note.txt
   fileContent: あなたのテストノート内容
   ```

4. **フローが動けば成功!**

### メリット
- ✅ ファイルシステム関連のエラーなし
- ✅ 手動でテストしやすい
- ✅ OpenAI → Parse → Notion の基本フローを確認できる

---

## 🔧 解決策2: n8n-nodes-fs の問題を解決

### 問題: Watch Notes Folder が動かない

#### 原因
- n8n-nodes-fs がインストールされていない
- Docker コンテナからローカルフォルダにアクセスできない
- ノードのバージョンが古い

#### 解決方法

**Step 1: n8n-nodes-fs のインストール確認**

n8n の設定画面で確認:
1. Settings → Community Nodes
2. `n8n-nodes-fs` が表示されているか確認
3. なければ「Install」で追加

または Docker の場合:

```bash
docker exec -it <n8n-container-name> npm install n8n-nodes-fs
docker restart <n8n-container-name>
```

**Step 2: ボリュームマウントの確認**

`docker-compose.yml` を確認:

```yaml
services:
  n8n:
    volumes:
      - n8n_data:/home/node/.n8n
      - C:\Users\stair\OneDrive\Documents\Notes:/data/notes  # 追加
```

そして Watch Notes Folder のパスを `/data/notes` に変更

**Step 3: 代替案 - Webhook で手動トリガー**

n8n-nodes-fs の代わりに、Webhook でファイル内容を受け取る:

```
[Webhook Trigger]
    ↓
[Extract File Data]
    ↓
[OpenAI Category Tagging]
    ↓
...
```

---

## 🔧 解決策3: Notion API のエラーを解決

### 問題: Get All Notes from Notion が動かない

#### 原因
- Notion Integration が設定されていない
- データベース ID が間違っている
- データベースに Integration が接続されていない

#### 解決方法

**Step 1: Notion Integration の作成**

1. https://www.notion.so/my-integrations にアクセス
2. 「New integration」をクリック
3. 名前を `n8n-notes` に設定
4. 「Submit」をクリック
5. **Internal Integration Token** をコピー

**Step 2: データベースに Integration を接続**

1. Notion でデータベースを開く
2. 右上の「...」→「Connections」
3. 作成した Integration (`n8n-notes`) を追加

**Step 3: データベース ID を取得**

1. Notion でデータベースを開く
2. URL をコピー: `https://notion.so/xxxxx?v=yyyyy`
3. `xxxxx` の部分がデータベース ID

**Step 4: n8n に設定**

1. Notion ノードをクリック
2. Credentials で「Create New」
3. Token を貼り付け
4. Database ID を設定

---

## 📝 どのエラーが出ているか確認する方法

### 1. ノードをクリック
エラーが出ているノードをクリックして詳細を確認

### 2. 実行ログを確認
1. 「Execute Workflow」をクリック
2. エラーメッセージを確認
3. エラーメッセージをコピーして教えてください

### 3. よくあるエラーメッセージ

| エラーメッセージ | 原因 | 解決方法 |
|----------------|------|---------|
| "Module not found: n8n-nodes-fs" | n8n-nodes-fs 未インストール | Docker で npm install |
| "ENOENT: no such file or directory" | パスが間違っている | ボリュームマウント確認 |
| "Unauthorized" | Notion API キーが間違っている | Integration Token 再確認 |
| "Database not found" | データベース ID が間違っている | URL から再取得 |
| "Integration not connected" | Integration がデータベースに未接続 | Connections から追加 |

---

## 🎯 次のステップ

### オプションA: 簡易版で動作確認(推奨)
1. `notes-to-notion-simple.json` をインポート
2. OpenAI と Notion の API キーを設定
3. 手動トリガーでテスト
4. 動けば基本フローは OK

### オプションB: エラー詳細を確認
1. エラーが出ているノードをクリック
2. エラーメッセージをコピー
3. 教えてください → 個別対応します

### オプションC: 段階的に構築
1. まず Start → OpenAI → Parse だけテスト
2. 動いたら Notion 登録を追加
3. 最後にファイル監視を追加

---

## 💡 おすすめの進め方

**まずは簡易版(`notes-to-notion-simple.json`)で基本フローを確認しましょう!**

1. ✅ OpenAI でカテゴリ/タグ生成が動く
2. ✅ Notion に登録できる
3. ✅ 基本フローが完成

この後、必要に応じてファイル監視や削除機能を追加できます。

---

**具体的なエラーメッセージを教えていただければ、ピンポイントで解決策を提示できます!**
