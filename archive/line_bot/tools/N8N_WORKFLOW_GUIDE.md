# ホゲーアルゴリズム n8n実装ガイド

n8nでホゲーアルゴリズムを完全自動化するワークフロー設計

## 全体構成

```
[トリガー] → [Python実行] → [投稿処理] → [反応取得] → [学習更新]
    ↓           ↓              ↓              ↓              ↓
 スケジュール  生成実行      X投稿/LINE    API取得      CSV更新
```

## ワークフロー詳細

### 1. トリガーノード

**ノードタイプ**: Schedule Trigger または Webhook

#### パターンA: 定期自動実行

```json
{
  "node": "Schedule Trigger",
  "parameters": {
    "rule": {
      "interval": [
        {
          "field": "hours",
          "hoursInterval": 3
        }
      ]
    }
  }
}
```

#### パターンB: 手動トリガー（Webhook）

```json
{
  "node": "Webhook",
  "parameters": {
    "path": "hogey-generate",
    "method": "POST",
    "responseMode": "lastNode"
  }
}
```

リクエスト例:
```bash
curl -X POST http://localhost:5678/webhook/hogey-generate \
  -H "Content-Type: application/json" \
  -d '{"theme": "貧乏脱出", "count": 5, "type": "buzz"}'
```

---

### 2. Function ノード（パラメータ準備）

```javascript
// テーマとカウントを設定
const theme = $input.item.json.theme || "人生逆転";
const count = $input.item.json.count || 10;
const postType = $input.item.json.type || "buzz"; // buzz or trilogy

return {
  json: {
    theme: theme,
    count: count,
    type: postType,
    timestamp: new Date().toISOString()
  }
};
```

---

### 3. Execute Command ノード（Python実行）

```json
{
  "node": "Execute Command",
  "parameters": {
    "command": "python",
    "arguments": [
      "hogey_algorithm.py",
      "--theme={{ $json.theme }}",
      "--count={{ $json.count }}",
      "--type={{ $json.type }}"
    ],
    "cwd": "c:\\Repos\\note-articles\\tools"
  }
}
```

#### hogey_algorithm.pyの修正（CLI対応）

```python
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--theme', default='人生逆転')
    parser.add_argument('--count', type=int, default=10)
    parser.add_argument('--type', default='buzz')
    args = parser.parse_args()
    
    hogey = HogeyAlgorithm()
    
    if args.type == 'trilogy':
        result = hogey.generate_story_trilogy(theme=args.theme)
        print(json.dumps(result, ensure_ascii=False))
    else:
        df = hogey.generate_posts_batch(count=args.count, theme=args.theme)
        hogey.save_posts_csv(df, 'generated_posts.csv')
        print(json.dumps(df.to_dict('records'), ensure_ascii=False))
```

---

### 4. 出力処理ノード（分岐）

#### 4-A. LINE通知ノード

```json
{
  "node": "LINE",
  "parameters": {
    "authentication": "oAuth2",
    "resource": "notification",
    "message": "🐶ホゲー投稿生成完了\n\n{{ $json.text }}\n\n教育: {{ $json.education_type }}\n予約: {{ $json.scheduled_datetime }}"
  }
}
```

#### 4-B. X (Twitter) 投稿ノード

```json
{
  "node": "Twitter",
  "parameters": {
    "resource": "tweet",
    "operation": "create",
    "text": "={{ $json.text }}"
  }
}
```

---

### 5. 反応取得ノード（定期実行）

**別ワークフロー推奨**: 投稿後24時間後に反応取得

```json
{
  "node": "Twitter",
  "parameters": {
    "resource": "tweet",
    "operation": "get",
    "tweetId": "={{ $json.tweet_id }}"
  }
}
```

取得データ:
- `public_metrics.like_count`
- `public_metrics.retweet_count`
- `public_metrics.reply_count`

---

### 6. CSV保存ノード

```json
{
  "node": "Spreadsheet File",
  "parameters": {
    "operation": "append",
    "filePath": "c:\\Repos\\note-articles\\tools\\my_posts.csv",
    "fileFormat": "csv",
    "options": {
      "headerRow": true
    }
  }
}
```

保存データ例:
```csv
post_id,text,datetime,likes,retweets,comments,hashtags
1,"残高274円の夜...",2025-01-08 12:00:00,150,30,5,#げすいぬ
```

---

### 7. 学習更新ノード（Python再実行）

```json
{
  "node": "Execute Command",
  "parameters": {
    "command": "python",
    "arguments": [
      "-c",
      "from hogey_algorithm import HogeyAlgorithm; h = HogeyAlgorithm(); h.learn_from_csv('my_posts.csv', 'bench_posts.csv'); print('学習完了')"
    ],
    "cwd": "c:\\Repos\\note-articles\\tools"
  }
}
```

---

## ワークフロー例（完全版）

### ワークフロー1: 投稿生成＆投稿

```
┌─────────────────┐
│ Schedule Trigger│  毎3時間実行
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Function Node  │  パラメータ設定
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Execute Command │  Python実行（投稿生成）
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   IF Node       │  投稿方法分岐
└────┬───────┬────┘
     │       │
     ▼       ▼
┌─────┐   ┌──────┐
│LINE │   │Twitter│
└─────┘   └───┬──┘
              │
              ▼
         ┌─────────┐
         │CSV保存  │
         └─────────┘
```

### ワークフロー2: 反応取得＆学習

```
┌─────────────────┐
│ Schedule Trigger│  毎日1回実行
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Twitter API     │  投稿リスト取得
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Loop Over      │  各投稿の反応取得
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  CSV追記        │  my_posts.csv更新
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Execute Command │  学習実行
└─────────────────┘
```

---

## 環境変数設定

n8nの環境変数に以下を設定:

```env
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_SECRET=your_access_secret
LINE_NOTIFY_TOKEN=your_line_token
HOGEY_WORKSPACE_PATH=c:\Repos\note-articles\tools
```

---

## トラブルシューティング

### Pythonが実行されない

**解決策**:
1. n8nの実行ユーザーでPythonが使えるか確認
2. `Execute Command`ノードのcwdを絶対パスに
3. PowerShellの場合は`python`ではなく`python.exe`を指定

```json
{
  "command": "C:\\Python311\\python.exe"
}
```

### CSVが保存されない

**解決策**:
1. ディレクトリの書き込み権限確認
2. パスの区切り文字を`\\`に統一（Windows）
3. UTF-8 BOMで保存

### LINE通知が届かない

**解決策**:
1. LINE Notify トークンの有効期限確認
2. メッセージ本文の改行コード確認（`\n`）
3. 文字数制限（1000文字以内）

---

## パフォーマンス最適化

### 1. バッチ処理

一度に10件生成してキューに貯める:

```javascript
// Function Node
const posts = JSON.parse($input.item.json.stdout);
return posts.map(post => ({ json: post }));
```

### 2. エラーハンドリング

```javascript
// Function Node (Try-Catch)
try {
  const result = JSON.parse($input.item.json.stdout);
  return { json: result };
} catch (error) {
  return { 
    json: { 
      error: error.message,
      fallback_text: "エラーが発生しました"
    }
  };
}
```

### 3. ログ記録

```json
{
  "node": "Spreadsheet File",
  "parameters": {
    "operation": "append",
    "filePath": "logs/hogey_execution.csv",
    "data": {
      "timestamp": "={{ $now }}",
      "theme": "={{ $json.theme }}",
      "count": "={{ $json.count }}",
      "status": "success"
    }
  }
}
```

---

## セキュリティ

### API トークンの保護

1. n8n Credentials機能を使用
2. 環境変数に格納（`.env`ファイル）
3. Git管理から除外（`.gitignore`）

```gitignore
.env
*.csv
generated_posts.csv
my_posts.csv
bench_posts.csv
```

---

## 次のステップ

1. ✅ ワークフロー1を作成して投稿生成テスト
2. ✅ LINE通知で動作確認
3. ✅ CSV学習データを10件程度準備
4. ✅ ワークフロー2で自動学習テスト
5. ✅ X投稿の自動化（慎重に）

---

**ホゲーアルゴリズムで泥人間の心を動かせ。**
