# プロンプト自動管理システム

Xで見つけた有益なプロンプトをLINEで送るだけで、Notionに自動整理されるシステムです。

## 🎯 特徴

- **完全無料**: LINE, Notion Free Plan, n8n Cloud Free Tier
- **スマホ完結**: LINEアプリだけで完結
- **自動分類**: AI自動タグ付け・カテゴリ分類
- **PC同期**: Notion経由で全デバイス同期
- **プログラミング不要**: n8nのビジュアルワークフロー
- **検索最適化**: タグ・カテゴリ・全文検索対応

## 📱 使い方（超シンプル）

1. **保存**: プロンプトをLINEに送信
   ```
   プロンプト: 
   あなたは優秀なマーケターです。
   ターゲット層を分析し...
   ```

2. **検索**: キーワードで検索
   ```
   検索 マーケティング
   ```

3. **一覧**: 最近の10件表示
   ```
   一覧
   ```

## 🛠️ セットアップ手順

### 1. Notion設定 (5分)

1. [Notion](https://www.notion.so/)でアカウント作成（無料）
2. 新規ページ作成「プロンプト管理DB」
3. データベースに変換（/database → Database - Inline）
4. 以下のプロパティを追加：
   - `プロンプト` (Text)
   - `カテゴリ` (Select): マーケティング, プログラミング, ライティング, ビジネス, その他
   - `タグ` (Multi-select)
   - `ソース` (URL)
   - `保存日時` (Created time)
   - `メモ` (Text)
   - `お気に入り` (Checkbox)

5. Notion API Integration作成:
   - [My integrations](https://www.notion.so/my-integrations)
   - 「New integration」
   - 名前: `プロンプト管理Bot`
   - Associated workspace: 自分のワークスペース
   - 「Submit」
   - **Internal Integration Token**をコピー（後で使用）

6. データベースに権限付与:
   - プロンプト管理DBページ右上「...」→「Connections」
   - 作成したIntegration「プロンプト管理Bot」を追加

7. **Database ID**を取得:
   - データベースページのURLをコピー
   - `https://www.notion.so/あなたのワークスペース/DATABASE_ID?v=...`
   - `DATABASE_ID`部分（32文字の英数字）をメモ

### 2. LINE Bot設定 (10分)

1. [LINE Developers](https://developers.line.biz/console/)でログイン
2. 新規プロバイダー作成「個人用Bot」
3. 新規チャネル作成:
   - チャネルの種類: Messaging API
   - チャネル名: `プロンプト管理Bot`
   - チャネル説明: `個人用プロンプト管理`
   - 大業種・小業種: 適当に選択
   - メールアドレス: 自分のアドレス
4. チャネル基本設定:
   - 「Messaging API設定」タブ
   - **Channel Secret**をコピー
   - **Channel Access Token**を発行してコピー
   - Webhook URL: `後で設定`（n8n URL）
   - Webhookの利用: `オン`
   - 応答メッセージ: `オフ`
   - Greeting messages: `オフ`
5. QRコードで友だち追加

### 3. n8n設定 (15分)

#### Option A: n8n Cloud（推奨・簡単）

1. [n8n Cloud](https://n8n.io/cloud/)で無料アカウント作成
   - Free tier: 月5,000実行まで無料
2. 新規ワークフロー作成「プロンプト管理」
3. 以下のワークフローをインポート（下記参照）
4. Webhook URLをコピー:
   - Webhookノードをクリック
   - 「Test URL」または「Production URL」をコピー
5. LINE Developersに戻り、Webhook URLに貼り付け

#### Option B: ローカルn8n（無料・無制限）

```powershell
# Docker Desktop必要（無料）
docker run -d --name n8n -p 5678:5678 -v C:\n8n_data:/home/node/.n8n n8nio/n8n

# ブラウザで http://localhost:5678 にアクセス
```

**ngrok**で外部公開（LINE Webhook用）:
```powershell
# ngrokインストール（無料）
choco install ngrok

# トンネル起動
ngrok http 5678

# 表示されたHTTPS URLをLINE Webhook URLに設定
# 例: https://xxxx-xxxx-xxxx.ngrok-free.app/webhook/line-prompt
```

### 4. n8nワークフロー設定

以下のノード構成を作成:

```
[Webhook] → [Switch] → [Notion] → [LINE Reply]
              ↓
         [検索/一覧]
```

**ワークフロー詳細は `workflow.json` を参照**

### 5. 認証情報設定

n8nで以下の認証情報を追加:

#### LINE認証
- Credential Type: `LINE`
- Channel Access Token: `（LINE Developersからコピー）`
- Channel Secret: `（LINE Developersからコピー）`

#### Notion認証
- Credential Type: `Notion API`
- API Key: `（Notion Integrationトークン）`
- Database ID: `（NotionデータベースID）`

## 🚀 使用例

### プロンプト保存
```
プロンプト: あなたは経験豊富なSEOコンサルタントです。
以下のブログ記事のタイトルを10個提案してください...

→ 自動でNotionに保存され、「マーケティング」「SEO」タグ付与
```

### カテゴリ指定保存
```
カテゴリ: プログラミング
プロンプト: Pythonでデータ分析するためのベストプラクティスを教えてください
```

### 検索
```
検索 SEO
→ SEO関連プロンプト一覧を返信
```

### タグ検索
```
タグ マーケティング
→ マーケティングタグの全プロンプト
```

### 最近の保存
```
一覧
→ 最新10件を表示
```

### お気に入り追加
```
お気に入り 3
→ 3番目のプロンプトをお気に入り登録
```

## 🎨 カスタマイズ

### カテゴリ追加
Notion DBの「カテゴリ」プロパティにオプション追加

### 自動タグ付けルール
n8nの「AI Categorize」ノードで以下を編集:
```javascript
// キーワードマッチング例
if (prompt.includes('マーケティング') || prompt.includes('SEO')) {
  category = 'マーケティング';
  tags.push('SEO', 'コンテンツ');
}
```

### Notion表示カスタマイズ
- ビュー追加（カレンダー、ギャラリー、タイムライン）
- フィルタ設定（お気に入りのみ、カテゴリ別）
- ソート（保存日時、カテゴリ）

## 📊 容量制限

| サービス | 無料枠 | 十分な理由 |
|---------|--------|------------|
| Notion Free | 1,000ブロック | プロンプト1件=1ブロック、1,000件保存可能 |
| n8n Cloud Free | 月5,000実行 | 1日166回送信可能（十分すぎる） |
| LINE Messaging API | 無料 | 個人利用は完全無料 |

### 容量超過時の対策
- Notion: アーカイブページに古いプロンプト移動（手動、月1回）
- n8n: ローカルDocker版に切り替え（無制限）

## 🔒 セキュリティ

- LINE Webhook検証: Channel Secretで署名検証済み
- Notion API: トークンは外部に漏らさない
- n8n: 認証情報は暗号化保存

## 🐛 トラブルシューティング

### LINEが反応しない
1. n8nワークフローが**Active**になっているか確認
2. LINE Webhook URLが正しいか確認
3. n8n実行履歴でエラーログ確認

### Notionに保存されない
1. Notion IntegrationがDBに接続されているか確認
2. Database IDが正しいか確認
3. n8n Notion認証情報を再設定

### ngrokが切れる（ローカルn8n使用時）
- ngrokは8時間で切断（無料版）
- 再起動して新URLをLINE Webhook URLに更新
- または有料版（$8/月）で固定URL使用

## 📝 note記事として販売する場合

### 記事タイトル案
- 「【完全無料】Xのプロンプトを自動整理！スマホだけで完結するLINE管理術」
- 「プロンプト管理を革命的に効率化！プログラミング不要のNotion×LINE連携」
- 「1,000個のプロンプトも埋もれない！スマホ5分で構築する自動管理システム」

### 記事構成例
1. 【共感】プロンプト管理の悩み（メモ帳がカオス、検索できない）
2. 【解決策】LINE×Notion自動管理システムの全貌
3. 【具体的手順】15分でできるセットアップ画像解説
4. 【実演】実際の使用シーン動画
5. 【応用】ビジネス活用・チーム共有の可能性
6. 【CTA】有料記事（¥500-980）またはテンプレート販売

### 差別化ポイント
- **完全無料**: 他の有料ツール不要
- **即効性**: 15分でセットアップ完了
- **再現性**: 画像+JSON付きで誰でも実装可能
- **拡張性**: タスク管理・メモ・ブックマークにも応用可能

## 🔄 メンテナンス

### 定期作業（推奨）
- **月1回**: Notionのアーカイブ整理（古いプロンプト移動）
- **3ヶ月に1回**: n8n実行ログ確認（エラーチェック）

### 完全自動化オプション
- Notion API + GitHub Actionsで週次バックアップ
- n8n Cronトリガーで月次アーカイブ自動化

## 💰 収益化戦略

1. **基本記事（無料）**: セットアップ手順の概要
2. **詳細版（¥500）**: 画像付き完全ガイド + n8nワークフローJSON
3. **プレミアム版（¥1,980）**: 
   - AI自動カテゴリ分類（ChatGPT API連携）
   - Slack/Discord連携版
   - チーム共有版
   - 1ヶ月サポート付き

## 📚 参考リンク

- [Notion API Documentation](https://developers.notion.com/)
- [LINE Messaging API](https://developers.line.biz/ja/docs/messaging-api/)
- [n8n Documentation](https://docs.n8n.io/)
- [ngrok Documentation](https://ngrok.com/docs)

---

**Version**: 1.0.0  
**最終更新**: 2025-11-16  
**作成者**: AI Narrative Studio
