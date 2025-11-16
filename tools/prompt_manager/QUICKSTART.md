# 🚀 クイックスタートガイド

15分で完結するセットアップ手順の簡略版です。

## ✅ 事前準備

必要なもの:
- [ ] Googleアカウント（Notion用）
- [ ] LINEアカウント
- [ ] メールアドレス（n8n用）
- [ ] PC（初回セットアップのみ）

所要時間: **合計15分**

---

## ステップ1: Notion（5分）

### 1-1. アカウント作成
```
1. https://www.notion.so/ にアクセス
2. 「Continue with Google」でサインアップ
```

### 1-2. データベース作成
```
1. 左サイドバー「+ New page」
2. ページ名「プロンプト管理DB」
3. /database → Database - Inline
```

### 1-3. プロパティ追加（右上「+」から）
- [x] プロンプト (Text)
- [x] カテゴリ (Select) - オプション: マーケティング, プログラミング, ライティング, ビジネス, その他
- [x] タグ (Multi-select)
- [x] ソース (URL)
- [x] 保存日時 (Created time)
- [x] メモ (Text)
- [x] お気に入り (Checkbox)

### 1-4. API Integration作成
```
1. https://www.notion.so/my-integrations にアクセス
2. 「+ New integration」
3. Name: プロンプト管理Bot
4. Submit
5. **Internal Integration Token**をコピー → メモ帳に保存
```

### 1-5. 権限付与
```
1. プロンプト管理DBページを開く
2. 右上「...」→「Connections」
3. 「プロンプト管理Bot」を追加
```

### 1-6. Database ID取得
```
1. データベースページのURLをコピー
   例: https://www.notion.so/workspace/DATABASE_ID?v=...
2. DATABASE_ID（32文字）をメモ帳に保存
```

**メモ帳の内容例**:
```
Notion Integration Token: secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
Database ID: 1234567890abcdef1234567890abcdef
```

---

## ステップ2: LINE Bot（10分）

### 2-1. アカウント作成
```
1. https://developers.line.biz/console/ にアクセス
2. LINEでログイン
```

### 2-2. プロバイダー作成
```
1. 「Create」→「Create a new provider」
2. Provider name: 個人用Bot
```

### 2-3. チャネル作成
```
1. 「Create a new channel」→「Messaging API」
2. Channel name: プロンプト管理Bot
3. Channel description: 個人用
4. Category: IT・テクノロジー
5. Email: 自分のメール
6. Create
```

### 2-4. 認証情報取得
```
1. 「Messaging API」タブ
2. Channel Secret → コピー → メモ帳に保存
3. Channel access token → Issue → コピー → メモ帳に保存
```

### 2-5. 設定変更
```
1. Use webhook: ON
2. Auto-reply messages: OFF（重要！）
3. Greeting messages: OFF
```

### 2-6. 友だち追加
```
1. 「Basic settings」タブ
2. QRコードをスマホでスキャン
```

**メモ帳に追加**:
```
LINE Channel Secret: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
LINE Channel Access Token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## ステップ3: n8n（15分）

### 3-1. アカウント作成
```
1. https://n8n.io/cloud/ にアクセス
2. 「Start free」
3. メールアドレスでサインアップ
```

### 3-2. ワークフロー作成
```
1. 「Workflows」→「Create new workflow」
2. 名前: プロンプト管理
```

### 3-3. ワークフローインポート
```
1. 右上メニュー（三本線）→「Import from File」
2. workflow.jsonを選択（このフォルダ内）
3. Import
```

### 3-4. 認証情報設定

#### Notion API
```
1. 左サイドバー「Credentials」
2. 「Add Credential」→「Notion API」
3. API Key: （メモ帳のIntegration Token）
4. Database ID: （メモ帳のDatabase ID）
5. Save
```

#### LINE API
```
1. 「Add Credential」→「LINE」
2. Channel Access Token: （メモ帳のLINE Token）
3. Channel Secret: （メモ帳のLINE Secret）
4. Save
```

### 3-5. Webhook URL取得
```
1. ワークフローの「LINE Webhook」ノードをクリック
2. 「Production URL」をコピー
   例: https://yourinstance.app.n8n.cloud/webhook/line-prompt
```

### 3-6. LINE Webhook設定
```
1. LINE Developers → Messaging API設定タブ
2. Webhook URL: （n8nのURL）を貼り付け
3. Update
4. Verify（成功確認）
```

### 3-7. ワークフロー有効化
```
1. n8nワークフロー右上
2. 「Inactive」トグルをクリック
3. 「Active」（緑色）に変更
```

---

## ✅ 動作テスト

### テスト1: プロンプト保存
LINEで送信:
```
プロンプト: テストプロンプトです
```

期待結果:
```
✅ プロンプトを保存しました！

カテゴリ: その他
タグ: 

Notionで確認できます。
```

### テスト2: Notion確認
1. Notionのプロンプト管理DBを開く
2. 「テストプロンプトです」が保存されているか確認

### テスト3: 一覧
LINEで送信:
```
一覧
```

期待結果:
```
📋 最新プロンプト 1件

1. [その他]
テストプロンプトです

Notionで確認できます。
```

---

## 🎉 完了！

すべてのテストが成功したら、セットアップ完了です！

次にやること:
1. 実際のプロンプトを5個保存してみる
2. 検索機能を試す（`検索 キーワード`）
3. Notionでカテゴリ分けをカスタマイズ
4. お気に入り機能を活用

---

## 🐛 トラブルシューティング

### LINE botが反応しない

#### 原因1: n8nワークフローがInactive
**解決策**: n8n右上のトグルを「Active」に変更

#### 原因2: Webhook URL未設定
**解決策**: LINE Developers → Messaging API → Webhook URL確認

#### 原因3: Auto-reply messagesがON
**解決策**: LINE Developers → Messaging API → Auto-reply messages OFF

### Notionに保存されない

#### 原因1: Database ID間違い
**解決策**: NotionデータベースURLを再確認

#### 原因2: Integration未接続
**解決策**: Notionページ → Connections → Integration追加確認

#### 原因3: n8n認証情報エラー
**解決策**: n8n Credentials → Notion API → 再設定

### エラーログ確認方法

#### n8n実行履歴
```
1. n8nワークフロー画面
2. 左サイドバー「Executions」
3. 最新の実行をクリック
4. エラーメッセージを確認
```

#### LINE Webhook検証
```
1. LINE Developers → Messaging API設定
2. Webhook URL → Verify
3. エラーメッセージ確認
```

---

## 📞 サポート

### 無料サポート
- [GitHub Issues](リンク予定)
- [Discord コミュニティ](リンク予定)

### 有料サポート（note記事購入者限定）
- メールサポート（1ヶ月・回数無制限）
- Zoom相談（30分・1回）

---

## 📚 次のステップ

1. [README.md](README.md) - システム詳細仕様
2. [note_article_template.md](note_article_template.md) - note記事テンプレート
3. [SCREENSHOT_GUIDE.md](SCREENSHOT_GUIDE.md) - スクリーンショット撮影ガイド

---

**所要時間**: 15分  
**難易度**: ⭐⭐☆☆☆（初心者可）  
**最終更新**: 2025-11-16
