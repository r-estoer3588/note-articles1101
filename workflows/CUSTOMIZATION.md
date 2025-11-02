# 🎨 カスタマイズガイド - OpenAI プロンプト & フロー拡張

## 🤖 OpenAI でカテゴリ/タグ自動生成の詳細

### 基本構成

```
[Set Note Metadata]
    ↓
[OpenAI Category Tagging]  ← AI でカテゴリとタグを生成
    ↓
[Parse AI Response]        ← JSON をパース
    ↓
[Format for Notion]        ← Notion 形式に変換
```

---

## 📝 OpenAI プロンプトのカスタマイズ例

**重要**: n8n 1.117.3 では `n8n-nodes-base.openAi` (typeVersion 1.3) を使用します。プロンプトは Messages フィールドに1つのメッセージとして設定します。

### パターン1: シンプルな分類(デフォルト)

OpenAI Category Tagging ノードの Messages 設定:

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

**JSON Output**: ✓ (チェックを入れる)

### パターン2: 技術特化

```
あなたは技術ドキュメント分類の専門家です。

【カテゴリ】
- フロントエンド
- バックエンド
- インフラ
- データベース
- セキュリティ
- その他

【タグの付け方】
- 技術スタック名(例: React, Python, Docker)
- 最大5個
- 英語推奨

【出力形式】
{
  "category": "カテゴリ名",
  "tags": ["tag1", "tag2", "tag3"],
  "difficulty": "初級|中級|上級"
}

ファイル名: {{ $json.fileName }}

内容:
{{ $json.fileContent }}
```

**JSON Output**: ✓

**Format for Notion ノードも変更が必要:**

Parse AI Response ノードで `difficulty` を渡すように修正:

```javascript
return {
  fileName: prevItem.json.fileName,
  fileContent: prevItem.json.fileContent,
  filePath: prevItem.json.filePath,
  createdDate: prevItem.json.createdDate,
  category: parsed.category || '未分類',
  tags: Array.isArray(parsed.tags) ? parsed.tags : [],
  difficulty: parsed.difficulty || '未設定'  // 新規追加
};
```

### パターン3: ビジネス用

```
あなたはビジネスノート分類の専門家です。

【カテゴリ】
- プロジェクト管理
- ミーティング議事録
- 顧客対応
- アイデア
- タスク
- ナレッジベース

【タグの付け方】
- プロジェクト名
- 関係者名
- 期限(あれば)
- 最大7個

【出力形式】
{
  "category": "カテゴリ名",
  "tags": ["tag1", "tag2"],
  "priority": "高|中|低",
  "actionRequired": true or false
}

ファイル名: {{ $json.fileName }}

内容:
{{ $json.fileContent }}
```

**JSON Output**: ✓

### パターン4: 学習ノート特化

```
あなたは学習ノート分類の専門家です。

【カテゴリ】
- プログラミング
- 英語学習
- 資格試験
- 読書ノート
- オンライン講座
- その他学習

【タグの付け方】
- トピック名
- 学習ソース(書籍名、講座名など)
- 理解度(理解した、要復習など)
- 最大5個

【出力形式】
{
  "category": "カテゴリ名",
  "tags": ["topic1", "topic2"],
  "source": "学習ソース",
  "reviewNeeded": true or false
}

ファイル名: {{ $json.fileName }}

内容:
{{ $json.fileContent }}
```

**JSON Output**: ✓

---

## 🔧 Parse AI Response のカスタマイズ

### デフォルト版(エラーハンドリング強化済み)

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

### ログ出力版(デバッグ用)

```javascript
const aiResponse = $input.item.json;
console.log('=== AI Response ===');
console.log(JSON.stringify(aiResponse, null, 2));

let parsed = {};
if (aiResponse.category && aiResponse.tags) {
  parsed = aiResponse;
} else if (typeof aiResponse === 'string') {
  parsed = JSON.parse(aiResponse);
} else {
  parsed = { category: '未分類', tags: [] };
}

console.log('=== Parsed JSON ===');
console.log(JSON.stringify(parsed, null, 2));

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

---

## 🎯 フロー拡張アイデア

### 1. ファイルタイプ別処理

```
[Watch Notes Folder]
    ↓
[Read Note File]
    ↓
[File Type Check (IF)]
    ├─ (TRUE: .md) → [Markdown Parser] → [OpenAI]
    └─ (FALSE: .txt) → [OpenAI]
```

**File Type Check ノード:**

```javascript
{{ $json.path.endsWith('.md') }}
```

### 2. 長文の要約を追加

```
[OpenAI Category Tagging]
    ↓
[Parse AI Response]
    ↓
[OpenAI Summarize]  ← 新規追加
    ↓
[Format for Notion]
```

**OpenAI Summarize のプロンプト:**

```json
{
  "role": "system",
  "content": "以下のノート内容を3行で要約してください。"
},
{
  "role": "user",
  "content": "{{ $json.fileContent }}"
}
```

### 3. 重要度判定を追加

```
[Parse AI Response]
    ↓
[Importance Check (OpenAI)]  ← 新規追加
    ↓
[Format for Notion]
```

**Importance Check のプロンプト:**

```json
{
  "role": "system",
  "content": "このノートの重要度を「高・中・低」で判定してください。\n\n【判定基準】\n- 高: すぐにアクションが必要、重要な決定事項\n- 中: 後で見返す価値あり\n- 低: メモ程度\n\n【出力形式】\n{\"importance\": \"高|中|低\", \"reason\": \"理由\"}"
}
```

### 4. 画像付きノートの処理

```
[Watch Notes Folder]
    ↓
[Read Note File]
    ↓
[Image Extractor]  ← 新規追加(画像リンクを抽出)
    ↓
[OpenAI Vision]    ← 画像を分析
    ↓
[Format for Notion]
```

---

## 📊 Notion プロパティのカスタマイズ

### 基本プロパティ

```
- Title: タイトル(必須)
- Category: テキスト
- Tags: マルチセレクト
- Processed: チェックボックス
```

### 拡張プロパティ例

```
- Title: タイトル
- Category: セレクト(選択肢: 技術メモ, 読書メモ, アイデア, ...)
- Tags: マルチセレクト
- Priority: セレクト(選択肢: 高, 中, 低)
- ActionRequired: チェックボックス
- ReviewNeeded: チェックボックス
- Source: テキスト(書籍名、URL など)
- Difficulty: セレクト(選択肢: 初級, 中級, 上級)
- CreatedDate: 日付
- Processed: チェックボックス
```

**Format for Notion ノードの設定:**

```json
{
  "assignments": [
    { "name": "title", "value": "={{ $json.fileName }}" },
    { "name": "content", "value": "={{ $json.fileContent }}" },
    { "name": "category", "value": "={{ $json.category }}" },
    { "name": "tags", "value": "={{ $json.tags }}", "type": "array" },
    { "name": "priority", "value": "={{ $json.priority }}" },
    { "name": "actionRequired", "value": "={{ $json.actionRequired }}", "type": "boolean" },
    { "name": "reviewNeeded", "value": "={{ $json.reviewNeeded }}", "type": "boolean" },
    { "name": "source", "value": "={{ $json.source }}" },
    { "name": "difficulty", "value": "={{ $json.difficulty }}" },
    { "name": "createdDate", "value": "={{ $json.createdDate }}" },
    { "name": "processed", "value": true, "type": "boolean" }
  ]
}
```

---

## 🔔 通知機能の追加

### Discord 通知

**Random Reminder の後に Discord ノードを追加:**

```json
{
  "webhookUrl": "https://discord.com/api/webhooks/...",
  "content": "📚 今日のおすすめノート\n\n**タイトル**: {{ $json.title }}\n**カテゴリ**: {{ $json.category }}\n**URL**: {{ $json.url }}"
}
```

### Slack 通知

```json
{
  "channel": "#notes-reminder",
  "text": "今日のおすすめノート: {{ $json.title }}",
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*{{ $json.title }}*\nカテゴリ: {{ $json.category }}\n<{{ $json.url }}|Notion で開く>"
      }
    }
  ]
}
```

### Email 通知

```json
{
  "to": "your-email@example.com",
  "subject": "今日のおすすめノート: {{ $json.title }}",
  "body": "タイトル: {{ $json.title }}\nカテゴリ: {{ $json.category }}\nURL: {{ $json.url }}"
}
```

---

## 🧪 テスト用プロンプト

### テスト1: 技術メモ

```
Docker と n8n の連携テスト

今日は Docker Compose で n8n を起動して、ローカルフォルダを監視する設定を試した。
volumes の設定で少し詰まったが、最終的に動作した。

次回はボリュームマウントのベストプラクティスを調べる。
```

**期待される出力:**

```json
{
  "category": "技術メモ",
  "tags": ["Docker", "n8n", "自動化"]
}
```

### テスト2: 読書メモ

```
「ゼロから作るDeep Learning」第3章

畳み込みニューラルネットワーク(CNN)の基礎を学んだ。
フィルタリングと畳み込み演算の仕組みが理解できた。

次章はプーリング層について。
```

**期待される出力:**

```json
{
  "category": "読書メモ",
  "tags": ["機械学習", "Deep Learning", "CNN", "書籍"]
}
```

---

## 📚 参考: OpenAI パラメータの意味

| パラメータ | 推奨値 | 説明 |
|-----------|--------|------|
| model | gpt-4o-mini | コスト効率が良い(gpt-4o より安い) |
| temperature | 0.3 | 低いほど安定した出力(0.0〜2.0) |
| max_tokens | 500 | カテゴリとタグなら十分 |
| response_format | json_object | JSON 形式を強制 |

---

**🎉 これでカスタマイズ完了!**

自分のワークフローに合わせて、プロンプトやノードを追加してください。
