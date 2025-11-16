# トラブルシューティングガイド

システムが動作しない場合の診断・解決方法を記載します。

## 🔍 問題診断フローチャート

```
LINEで送信
  ↓
ボットが反応しない？
  ├─ YES → [セクション1: LINE Webhook問題]
  └─ NO
      ↓
    エラーメッセージが返る？
      ├─ YES → [セクション2: n8n処理エラー]
      └─ NO
          ↓
        Notionに保存されない？
          ├─ YES → [セクション3: Notion連携問題]
          └─ NO
              ↓
            検索・一覧が動作しない？
              └─ YES → [セクション4: 機能別問題]
```

---

## セクション1: LINE Webhook問題

### 症状: ボットが全く反応しない

#### チェック1: n8nワークフローの状態

**確認方法**:
```
1. n8nワークフロー画面を開く
2. 右上のトグルを確認
```

**期待値**: `Active`（緑色）

**解決策**:
```
Inactiveの場合 → トグルをクリックして「Active」に変更
```

---

#### チェック2: Webhook URL設定

**確認方法**:
```
1. n8nワークフロー → 「LINE Webhook」ノードをクリック
2. Production URLをコピー

3. LINE Developers → Messaging API設定タブ
4. Webhook URLを確認
```

**期待値**: n8nのURLとLINEのURLが一致

**解決策**:
```
不一致の場合 → LINE Developersで正しいURLに更新
```

---

#### チェック3: Webhook検証

**確認方法**:
```
LINE Developers → Messaging API設定タブ → Webhook URL → 「Verify」
```

**期待値**: `Success`メッセージ

**解決策（エラーの場合）**:

| エラー | 原因 | 解決策 |
|--------|------|--------|
| Connection failed | n8nがダウン | n8n Cloudのステータス確認 |
| Invalid signature | Channel Secret不一致 | n8n認証情報を再設定 |
| Timeout | ワークフロー処理が遅い | ノード削減・最適化 |

---

#### チェック4: Auto-reply設定

**確認方法**:
```
LINE Developers → Messaging API設定タブ
```

**期待値**:
- `Use webhook`: **ON**
- `Auto-reply messages`: **OFF**
- `Greeting messages`: **OFF**

**解決策**:
```
OFFになっていない場合 → 手動でOFFに変更
※Auto-reply ONだと自動応答が優先されてWebhookが無視される
```

---

#### チェック5: ngrok接続（ローカルn8n使用時のみ）

**確認方法**:
```powershell
# PowerShellで実行
curl https://xxxx-xxxx-xxxx.ngrok-free.app/webhook/line-prompt
```

**期待値**: HTTPステータス 200 または 405

**解決策**:
```
接続エラーの場合:
1. ngrokが起動しているか確認（ngrok http 5678）
2. URLが最新か確認（ngrokは8時間で切断）
3. LINE Webhook URLを新URLに更新
```

---

## セクション2: n8n処理エラー

### 症状: エラーメッセージが返る

#### チェック1: 実行履歴確認

**確認方法**:
```
1. n8nワークフロー画面
2. 左サイドバー「Executions」
3. 最新の実行（赤色=エラー）をクリック
4. エラーノードを確認
```

#### エラーパターン別解決策

##### エラー: "Missing credentials"

**原因**: 認証情報未設定

**解決策**:
```
1. n8n → Credentials → 該当サービス
2. API Key / Token を再入力
3. 「Save」
```

---

##### エラー: "Database not found"

**原因**: Notion Database ID不正

**解決策**:
```
1. NotionデータベースURLを再確認
   https://www.notion.so/workspace/DATABASE_ID?v=...
2. DATABASE_ID（32文字）をコピー
3. n8n → Credentials → Notion API → Database ID更新
```

---

##### エラー: "Unauthorized"

**原因**: API Token期限切れ or 権限不足

**解決策（Notion）**:
```
1. Notion → My integrations → Integration確認
2. トークンが有効か確認
3. データベースにConnectionが付与されているか確認
```

**解決策（LINE）**:
```
1. LINE Developers → Messaging API
2. Channel access tokenを再発行
3. n8n認証情報を更新
```

---

##### エラー: "Function execution failed"

**原因**: Functionノードのコードエラー

**解決策**:
```
1. エラーが出たFunctionノードをクリック
2. コンソールログ確認
3. 該当行のコードを修正

よくあるエラー:
- undefined property → null check追加
- invalid JSON → JSON.parse()エラーハンドリング
```

---

## セクション3: Notion連携問題

### 症状: Notionに保存されない（エラーなし）

#### チェック1: Integration接続

**確認方法**:
```
1. Notionプロンプト管理DBページを開く
2. 右上「...」→「Connections」
3. 「プロンプト管理Bot」が表示されているか
```

**解決策**:
```
表示されていない場合:
1. 「Add connections」
2. 「プロンプト管理Bot」を検索
3. 追加
```

---

#### チェック2: プロパティ名一致

**確認方法**:
```
Notionデータベースのプロパティ名確認
```

**期待値**:
- プロンプト (Text)
- カテゴリ (Select)
- タグ (Multi-select)
- メモ (Text)

**解決策**:
```
プロパティ名が異なる場合:
1. n8nワークフロー → Notion保存ノード
2. Properties設定でプロパティ名を修正

または

1. Notionデータベースでプロパティ名を変更
```

---

#### チェック3: Database ID確認

**確認方法**:
```
1. NotionデータベースURLをコピー
   https://www.notion.so/workspace-name/DATABASE_ID?v=view_id
2. DATABASE_ID部分を確認
```

**解決策**:
```
1. 正しいDatabase IDをコピー
2. n8n → Credentials → Notion API → Database ID更新
3. Save
```

---

## セクション4: 機能別問題

### 症状: 検索が動作しない

#### チェック1: 検索クエリ形式

**確認方法**:
```
LINEで送信: 検索 マーケティング
               ↑空白必須
```

**期待値**: 「検索」の後に半角スペース

**解決策**:
```
全角スペースの場合 → 半角スペースに修正
または
n8nワークフローのSwitch条件を全角対応に変更
```

---

#### チェック2: Notion検索フィルタ

**確認方法**:
```
n8nワークフロー → 「Notion検索」ノード → Filters設定確認
```

**期待値**:
```json
{
  "property": "プロンプト",
  "condition": "contains",
  "value": "={{ $json.keyword }}"
}
```

---

### 症状: 一覧が空

#### チェック1: Notion内データ確認

**確認方法**:
```
Notionプロンプト管理DBを開く
```

**期待値**: 1件以上のデータが存在

**解決策**:
```
データがない場合:
1. テストプロンプトを1件保存
2. 再度「一覧」を実行
```

---

#### チェック2: ソート設定

**確認方法**:
```
n8nワークフロー → 「Notion最新取得」ノード → Sort設定確認
```

**期待値**:
```json
{
  "property": "保存日時",
  "direction": "descending"
}
```

---

### 症状: カテゴリ自動分類が動作しない

#### チェック1: Functionノードのロジック

**確認方法**:
```
n8nワークフロー → 「プロンプト解析」ノード → Code確認
```

**期待値**:
```javascript
if (prompt.match(/マーケティング|SEO|広告/)) {
  category = 'マーケティング';
}
```

**解決策**:
```
キーワード追加例:
if (prompt.match(/マーケティング|SEO|広告|集客|SNS/)) {
  category = 'マーケティング';
  tags.push('マーケティング');
}
```

---

## 🚨 緊急時の対応

### システム全体がダウンした場合

#### 対応1: n8n Cloudステータス確認
```
https://status.n8n.io/
```

#### 対応2: LINE Messagingステータス確認
```
https://status.line.me/
```

#### 対応3: Notion APIステータス確認
```
https://status.notion.so/
```

---

### データバックアップ

#### Notionエクスポート（手動）
```
1. プロンプト管理DBページ
2. 右上「...」→「Export」
3. Format: Markdown & CSV
4. Export
```

#### n8nワークフローバックアップ
```
1. n8nワークフロー画面
2. 右上メニュー → Export workflow
3. JSONファイル保存
```

---

## 📞 サポートリソース

### 公式ドキュメント

- [Notion API Docs](https://developers.notion.com/)
- [LINE Messaging API Docs](https://developers.line.biz/ja/docs/messaging-api/)
- [n8n Documentation](https://docs.n8n.io/)

### コミュニティ

- n8n Community Forum: https://community.n8n.io/
- LINE Developers Community: https://www.line-community.me/

### 有料サポート（note記事購入者限定）

- メールサポート: support@example.com（1ヶ月無制限）
- Zoom相談: 30分（事前予約制）

---

## 📋 診断チェックリスト

問題発生時に上から順に確認してください：

- [ ] n8nワークフローが「Active」
- [ ] LINE Webhook URLが正しい
- [ ] LINE Auto-reply messagesが「OFF」
- [ ] Notion Integrationが接続されている
- [ ] n8n認証情報が正しい（Notion + LINE）
- [ ] NotionプロパティJSONが一致
- [ ] n8n実行履歴でエラー確認
- [ ] LINE Webhook検証が「Success」
- [ ] Notionに手動でデータ追加可能

すべてチェックしても解決しない場合:
1. システムを最初から再構築（15分）
2. 有料サポートに問い合わせ

---

**最終更新**: 2025-11-16
