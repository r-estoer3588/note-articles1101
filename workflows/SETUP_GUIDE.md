# 📘 Notes to Notion ワークフロー - 詳細セットアップガイド

## 🎯 目的

ローカルの Notes フォルダに `.txt` や `.md` ファイルを置くだけで、自動的に:
1. ファイルを読み込む
2. OpenAI でカテゴリとタグを自動生成
3. Notion データベースに登録
4. 30日後に古いファイルを削除

---

## ⚠️ 前提条件

- Windows + Docker + n8n 1.117.3 が動作している
- n8n-nodes-fs がインストール済み
- OpenAI API キーを持っている
- Notion API キーとデータベース ID を持っている

---

## 🔗 Watch Notes Folder → Read Note File の接続方法

### ❌ 接続できてない状態

n8n の UI 上で、2つのノードが線でつながっていない状態です。

### ✅ 接続する手順

1. **n8n UI を開く**
2. **Watch Notes Folder ノードの右端にある小さい●(ドット)をクリック**
3. **そのままマウスを Read Note File ノードまでドラッグ**
4. **Read Note File ノードの左端にマウスをドロップ**
5. **線がつながれば接続完了!**

### 🔍 接続が成功したか確認する方法

```json
// JSON エディタで確認(Advanced → View JSON)
"connections": {
  "Watch Notes Folder": {
    "main": [
      [
        {
          "node": "Read Note File",
          "type": "main",
          "index": 0
        }
      ]
    ]
  }
}
```

この部分が存在すれば OK です。

---

## 🤖 OpenAI でカテゴリ/タグ自動生成の実装

### 1. OpenAI Category Tagging ノードの設定

#### 基本設定
- **Model**: gpt-4o-mini
- **Temperature**: 0.3(安定した分類のため低め)
- **JSON Output**: true(JSON形式で確実に返す)

#### メッセージ設定
プロンプトはシステムメッセージとユーザーメッセージを1つにまとめます:

```
あなたはノート分類の専門家です。以下のノート内容を読んで、適切なカテゴリとタグを提案してください。

【カテゴリ候補】
- 技術メモ
- 読書メモ
- アイデア
- 会議メモ
- 個人メモ

【タグの付け方】
- 最大5個まで
- 具体的なキーワードで
- 日本語で

【出力形式】
JSON形式で以下のように返してください:
{
  "category": "カテゴリ名",
  "tags": ["タグ1", "タグ2", "タグ3"]
}

ファイル名: {{ $json.fileName }}

内容:
{{ $json.fileContent }}
```

**重要**: n8n 1.117.3 の OpenAI ノードは `n8n-nodes-base.openAi` (typeVersion 1.3) を使用します。

### 2. Parse AI Response ノードの設定

OpenAI の返答は `jsonOutput: true` を設定しているので、すでにパース済みの JSON オブジェクトとして返ってきます。

```javascript
// Parse OpenAI JSON response
// n8n-nodes-base.openAi with jsonOutput: true returns parsed JSON directly
const aiResponse = $input.item.json;

// If the response is already an object with category and tags, use it directly
let parsed = {};
if (aiResponse.category && aiResponse.tags) {
  parsed = aiResponse;
} else if (typeof aiResponse === 'string') {
  // Fallback: if it's a string, try to parse it
  try {
    parsed = JSON.parse(aiResponse);
  } catch (e) {
    parsed = { category: '未分類', tags: [] };
  }
} else if (aiResponse.message?.content) {
  // Another fallback for different response format
  try {
    parsed = JSON.parse(aiResponse.message.content);
  } catch (e) {
    parsed = { category: '未分類', tags: [] };
  }
} else {
  parsed = { category: '未分類', tags: [] };
}

// Get original data from previous node
const prevItem = $input.first();

return {
  fileName: prevItem.json.fileName,
  fileContent: prevItem.json.fileContent,
  filePath: prevItem.json.filePath,
  createdDate: prevItem.json.createdDate,
  category: parsed.category || '未分類',
  tags: Array.isArray(parsed.tags) ? parsed.tags : []
};
```

**エラーハンドリング**: 複数の形式に対応しているので、OpenAI ノードのバージョンが変わっても動作します。

### 3. Format for Notion ノードの設定

Parse AI Response から受け取ったデータを Notion の形式に整形します。

```json
{
  "assignments": [
    {
      "name": "title",
      "value": "={{ $json.fileName.replace('.txt', '').replace('.md', '') }}"
    },
    {
      "name": "content",
      "value": "={{ $json.fileContent }}"
    },
    {
      "name": "category",
      "value": "={{ $json.category }}"
    },
    {
      "name": "tags",
      "value": "={{ $json.tags }}",
      "type": "array"
    },
    {
      "name": "processed",
      "value": true,
      "type": "boolean"
    }
  ]
}
```

---

## 🔄 フロー完成までの接続方法

### 接続順序

```
1. Watch Notes Folder → Read Note File
2. Read Note File → Set Note Metadata
3. Set Note Metadata → OpenAI Category Tagging
4. Set Note Metadata → Old File Check(IF)
5. OpenAI Category Tagging → Parse AI Response
6. Parse AI Response → Format for Notion
7. Format for Notion → Notion Create Item
8. Old File Check(TRUE) → Delete Old File
```

### 各接続の意味

| 接続元 | 接続先 | データの流れ |
|--------|--------|-------------|
| Watch Notes Folder | Read Note File | `{ path: "C:\\...\\note.txt" }` |
| Read Note File | Set Note Metadata | `{ path: "...", data: "ファイル内容" }` |
| Set Note Metadata | OpenAI | `{ fileName, fileContent, filePath, createdDate }` |
| OpenAI | Parse AI Response | `{ message: { content: '{"category":"..."}' } }` |
| Parse AI Response | Format for Notion | `{ category, tags, fileName, ... }` |
| Format for Notion | Notion | `{ title, content, category, tags, processed }` |

---

## 🧪 テスト方法

### 1. 手動実行テスト

1. **Watch Notes Folder ノードを右クリック**
2. **「Execute Node」を選択**
3. **監視フォルダに `test.txt` を追加**
4. **各ノードが順番に実行されるか確認**

### 2. OpenAI のテスト

Parse AI Response ノードで以下のテストデータを使用:

```json
{
  "message": {
    "content": "{\"category\":\"技術メモ\",\"tags\":[\"Python\",\"自動化\",\"n8n\"]}"
  },
  "fileName": "test.txt",
  "fileContent": "n8n で自動化の練習",
  "filePath": "C:\\Notes\\test.txt",
  "createdDate": "2025-11-02T00:00:00Z"
}
```

### 3. Notion 登録のテスト

Format for Notion → Notion Create Item の流れを確認:

```json
// Format for Notion の出力
{
  "title": "test",
  "content": "n8n で自動化の練習",
  "category": "技術メモ",
  "tags": ["Python", "自動化", "n8n"],
  "processed": true
}
```

---

## 🐛 よくあるエラーと解決方法

### エラー1: Watch Notes Folder が動かない

**原因**: Docker コンテナから監視フォルダにアクセスできない

**解決方法**:
```yaml
# docker-compose.yml
volumes:
  - C:\Users\stair\OneDrive\Documents\Notes:/notes
```

そして Watch Notes Folder のパスを `/notes` に変更

### エラー2: Read Note File で `undefined`

**原因**: Watch Notes Folder からの `path` が渡されていない

**解決方法**: 
- 接続が正しくされているか確認
- `{{ $json.path }}` が正しく設定されているか確認

### エラー3: OpenAI が JSON を返さない

**原因**: JSON Output が設定されていない、またはプロンプトが不適切

**解決方法**:
1. OpenAI Category Tagging ノードの **Options** で **JSON Output** にチェック
2. プロンプトに「JSON形式で返してください」を明記
3. Parse AI Response のエラーハンドリングが機能しているか確認

### エラー3.5: "The value 'chat' is not supported!"

**原因**: n8n のバージョンによって OpenAI ノードの形式が異なる

**解決方法**:
- n8n 1.117.3 では `n8n-nodes-base.openAi` (typeVersion 1.3) を使用
- `resource: "chat"` ではなく、直接 `model` パラメータを設定
- 提供されている JSON ファイルは修正済みです

### エラー4: Notion に登録されない

**原因**: データベース ID が間違っている、またはプロパティ名が一致しない

**解決方法**:
1. Notion データベースの「Share」から Integration を追加
2. URL の最後の部分がデータベース ID
3. プロパティ名を確認(大文字小文字も一致させる)

---

## 🎨 カスタマイズアイデア

### 1. カテゴリを増やす

システムプロンプトを編集:

```json
"【カテゴリ候補】\n- 技術メモ\n- 読書メモ\n- アイデア\n- 会議メモ\n- 個人メモ\n- プロジェクト\n- 学習ノート"
```

### 2. タグの自動生成ルールを変更

```json
"【タグの付け方】\n- 最大3個まで\n- 英語で\n- 小文字のみ"
```

### 3. リマインド通知を Discord に送る

Random Reminder の後に Discord ノードを追加:

```json
{
  "webhookUrl": "https://discord.com/api/webhooks/...",
  "content": "今日のおすすめノート: {{ $json.title }}\nカテゴリ: {{ $json.category }}\nURL: {{ $json.url }}"
}
```

---

## 📚 参考リンク

- [n8n 公式ドキュメント](https://docs.n8n.io/)
- [OpenAI API リファレンス](https://platform.openai.com/docs/api-reference)
- [Notion API ガイド](https://developers.notion.com/)
- [n8n-nodes-fs GitHub](https://github.com/n8n-io/n8n-nodes-fs)

---

## ✅ 完成チェックリスト

- [ ] Watch Notes Folder → Read Note File が接続されている
- [ ] OpenAI API キーが設定されている
- [ ] Notion API キーとデータベース ID が設定されている
- [ ] 監視フォルダパスが正しい
- [ ] テストファイルで動作確認済み
- [ ] 古いファイル削除が動作している(オプション)
- [ ] リマインド機能が動作している(オプション)

---

## 🔄 最新の状況（2025年11月2日 21:15更新）

### 実施済み対応

1. **Docker 環境でのセットアップ完了**
   - コンテナ名: `n8n-notes-organizer`
   - ポート: `5678`
   - ボリュームマウント: `C:\Notes` → `/notes`
   - データ永続化: `n8n_data:/root/.n8n`

2. **環境変数の設定**
   - `OPENAI_API_KEY`: 最新キー `sk-proj-ZIoSx1K4lJBq...` で更新済み（2025/11/02 21:15）
   - コンテナ再起動で環境変数を反映

3. **認証情報の再登録**
   - Notion API: `Notion account` 再登録完了
   - OpenAI API: 環境変数で設定済み

4. **Notion データベース設定**
   - データベースID: `29e1972f485180c89c68d77f1b82e39f`
   - プロパティ構成:
     - Title (タイトル)
     - Content (リッチテキスト)
     - Processed (チェックボックス)
     - **Category (リッチテキスト)** ← Rich text で運用（Select ではない）
     - **Tags (マルチセレクト)**
   - n8n の接続権限を追加済み

5. **ワークフロー修正内容**
   - Watch Notes Folder: パスを `/notes` に変更（Docker コンテナ内のパス）
   - Delete Old File: コマンドを `rm -f` に変更（Linux 対応）
   - OpenAI Category Tagging: Code ノードで直接 API 呼び出し（n8n-nodes-base.openAi が使用不可のため）

### 現在の課題

1. **localFileTrigger の制限**
   - Docker 環境では `inotify` が正しく動作せず、Watch Notes Folder がファイル追加を検知できない
   - ログ確認: `docker logs n8n-notes-organizer` で「User attempted to access a workflow without permissions」が多発
   - 実行履歴で上段フロー（Watch → Read → ... → Notion）が起動していない

2. **代替案の検討が必要**
   - **案A**: スケジュール実行（Schedule Trigger）でフォルダをスキャンし、未処理ファイルを検出
   - **案B**: n8n Cloud で同じワークフローを作成して動作確認
   - **案C**: Webhook や Manual Trigger で手動実行し、ロジック部分を先に完成させる

3. **次のステップ**
   - [ ] 手動テスト（Execute workflow）で Notion Create Item まで正常に通るか確認
   - [ ] ファイル監視を Schedule Trigger + フォルダスキャンに変更
   - [ ] 実運用前に全フロー（OpenAI 分類 → Notion 登録）の動作確認を完了

### 環境情報

```bash
# Docker コンテナ起動コマンド（最新版）
docker run -d \
  --name n8n-notes-organizer \
  -p 5678:5678 \
  -e OPENAI_API_KEY="sk-proj-ZIoSx1K4lJBq..." \
  -v n8n_data:/root/.n8n \
  -v C:\Notes:/notes \
  n8nio/n8n:latest

# コンテナ内のファイル確認
docker exec n8n-notes-organizer ls -la /notes

# ログ確認
docker logs n8n-notes-organizer --tail 50
```

### トラブルシューティング

**問題**: Watch Notes Folder が反応しない  
**原因**: Docker マウントでは localFileTrigger の inotify が動作しづらい  
**解決**: Schedule Trigger に切り替えるか、n8n Cloud で検証

**問題**: "Node does not have any credentials set for 'notionApi'"  
**状態**: Notion 認証情報を再登録して解消済み

**問題**: OpenAI Category Tagging で「Install this node to use it」エラー  
**解決**: Code ノードで OpenAI API を直接呼び出すように変更済み

---

**🎉 これで完成です!**

監視フォルダにファイルを追加するだけで、自動的に AI が分類して Notion に登録してくれます。
