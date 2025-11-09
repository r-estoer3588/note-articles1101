# n8n 半自動投稿ワークフロー設計
対象: AI Narrative Studio & GETHNOTE

---

## ワークフロー概要

```
Notion投稿DB → 今日の投稿取得 → Slack通知 → 人間承認 → X投稿 → ステータス更新
```

---

## 必要なもの

1. **n8n**（セルフホスト or n8n.cloud）
2. **Notion** or **Airtable**（投稿ストック管理）
3. **Slack** or **Discord**（承認通知）
4. **X API v2 Bearer Token**（投稿用）

---

## Notionデータベース構造

### 投稿ストックDB

| プロパティ | 型 | 説明 |
|-----------|-----|------|
| タイトル | Text | 投稿の概要 |
| 本文 | Text | 投稿本文（280文字以内） |
| アカウント | Select | AI_Narrative / GETHNOTE |
| 投稿予定日 | Date | いつ投稿するか |
| ステータス | Select | 下書き / 承認済み / 投稿済み |
| カテゴリ | Select | 体験談 / 問いかけ / データ / Tips / ニュース |
| 画像URL | URL | 添付画像（オプション） |

---

## n8nワークフロー詳細

### ノード1: Cron（トリガー）
```
設定:
- 実行時間: 毎日 20:50（AI Narrative）/ 22:50（GETHNOTE）
- タイムゾーン: Asia/Tokyo
```

### ノード2: Notion - Get Database Items
```
設定:
- Database: 投稿ストックDB
- Filter:
  - 投稿予定日 = 今日
  - ステータス = 承認済み
  - アカウント = AI_Narrative（または GETHNOTE）
- Limit: 1
```

### ノード3: IF - 投稿があるかチェック
```
条件:
- {{ $json.length > 0 }}
```

### ノード4: Slack - Send Message
```
設定:
- Channel: #x-投稿承認
- Message:
  """
  🔔 投稿準備完了！
  
  【アカウント】{{ $json.アカウント }}
  【カテゴリ】{{ $json.カテゴリ }}
  
  【本文】
  {{ $json.本文 }}
  
  この内容で投稿しますか？
  ✅ リアクションで承認
  ❌ リアクションでスキップ
  """
- Attachments: {{ $json.画像URL }}（あれば）
```

### ノード5: Slack - Wait for Reaction
```
設定:
- Message ID: {{ $json.message_id }}
- Wait for: emoji_added
- Timeout: 10分
```

### ノード6: Switch - リアクションで分岐
```
条件:
- ✅ → ノード7へ
- ❌ → ノード10へ（スキップ通知）
- Timeout → ノード10へ
```

### ノード7: X API - Create Tweet
```
設定:
- Method: POST
- Endpoint: https://api.twitter.com/2/tweets
- Authentication: Bearer Token
- Body:
  {
    "text": "{{ $json.本文 }}"
  }
```

### ノード8: Notion - Update Page
```
設定:
- Page ID: {{ $json.id }}
- Properties:
  - ステータス: 投稿済み
  - 投稿日時: {{ $now }}
  - 投稿ID: {{ $json.tweet_id }}
```

### ノード9: Slack - Success通知
```
Message:
"""
✅ 投稿完了しました！

【アカウント】{{ $json.アカウント }}
【投稿ID】{{ $json.tweet_id }}
【URL】https://x.com/username/status/{{ $json.tweet_id }}
"""
```

### ノード10: Slack - スキップ通知
```
Message:
"""
⏭️ 投稿をスキップしました

【理由】タイムアウト or ❌リアクション
【次回】明日の同時刻に再度通知します
"""
```

---

## エラーハンドリング

### ノード11: Error Trigger
```
全ノードでエラーが発生したらここに来る
```

### ノード12: Slack - Error通知
```
Message:
"""
🚨 エラー発生！

【ワークフロー】X投稿自動化
【エラー内容】{{ $json.error }}
【対処】手動で投稿してください

投稿ストックを確認👇
https://notion.so/your-database
"""
```

---

## セキュリティ考慮事項

### 1. Bearer Token管理
```
❌ ワークフローに直接記載
✅ n8nのCredentials機能で管理
✅ 環境変数で管理
```

### 2. Notion/Slackアクセス制限
```
✅ 自分だけがアクセス可能に
✅ Webhook URLを外部に漏らさない
```

### 3. ログ管理
```
✅ 投稿ログをNotionに記録
✅ エラーログをSlackに通知
✅ 月次で振り返り
```

---

## 運用フロー

### 日曜夜（準備）
1. Notionで翌週7投稿を作成
2. ステータスを「承認済み」に変更
3. 投稿予定日を設定（月〜日）

### 月〜日（自動実行）
1. 20:50（AI Narrative）または22:50（GETHNOTE）にSlack通知
2. 10分以内に✅リアクション
3. 自動で投稿＆ステータス更新

### トラブル時
- タイムアウト → 翌日再通知
- エラー → Slack通知 → 手動投稿

---

## メリット・デメリット

### メリット
✅ 人間の最終確認あり（規約的に安全）
✅ 柔軟性高い（投稿前に変更可能）
✅ ログが残る（Notion・Slack）
✅ エラー時も対処できる

### デメリット
⚠️ 初期セットアップが少し複雑
⚠️ Slack通知に10分以内に反応必要
⚠️ n8nの維持が必要（セルフホスト時）

---

## 完全自動化版（自己責任）

上記ワークフローから以下を削除:
- ノード4（Slack通知）
- ノード5（Wait for Reaction）
- ノード6（Switch）

→ 直接ノード7（X投稿）に繋ぐ

**注意**: これは完全自動なのでリスク高め。
