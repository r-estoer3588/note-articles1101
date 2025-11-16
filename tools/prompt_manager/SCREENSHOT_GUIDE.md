# セットアップ画像ガイド（スクリーンショット撮影用）

このドキュメントは、note記事用のスクリーンショットを撮影する際のガイドです。

## 📸 必要なスクリーンショット一覧

### 1. Notion設定（5枚）

#### 1-1. Notionアカウント作成
- URL: https://www.notion.so/
- 撮影内容: サインアップ画面
- ポイント: 「Continue with Google」ボタンを矢印で強調

#### 1-2. データベース作成
- 撮影内容: 新規ページ → `/database` → `Database - Inline` 選択
- ポイント: コマンドパレットのスクリーンショット

#### 1-3. プロパティ設定
- 撮影内容: 完成したデータベーススキーマ
- 表示プロパティ:
  - プロンプト (Text)
  - カテゴリ (Select): マーケティング, プログラミング, ライティング, ビジネス, その他
  - タグ (Multi-select)
  - ソース (URL)
  - 保存日時 (Created time)
  - メモ (Text)
  - お気に入り (Checkbox)

#### 1-4. Integration作成
- URL: https://www.notion.so/my-integrations
- 撮影内容: 「New integration」→ 名前入力 → Submit
- ポイント: **Internal Integration Token**をモザイク処理して矢印で強調

#### 1-5. 権限付与
- 撮影内容: データベースページ右上「...」→「Connections」→ Integration追加
- ポイント: 「プロンプト管理Bot」が追加された状態

### 2. LINE Bot設定（6枚）

#### 2-1. LINE Developersログイン
- URL: https://developers.line.biz/console/
- 撮影内容: コンソール画面

#### 2-2. プロバイダー作成
- 撮影内容: 「Create」→「Create a new provider」
- ポイント: Provider名「個人用Bot」

#### 2-3. チャネル作成
- 撮影内容: Messaging API選択画面
- ポイント: アイコンを強調

#### 2-4. チャネル情報入力
- 撮影内容: チャネル名「プロンプト管理Bot」入力画面
- ポイント: 必須項目を埋めた状態

#### 2-5. 認証情報取得
- 撮影内容: Messaging API設定タブ
- ポイント:
  - **Channel Secret**（モザイク処理）
  - **Channel Access Token**（モザイク処理）
  - Webhook URLは「後で設定」

#### 2-6. QRコード友だち追加
- 撮影内容: Basic settings → QRコード
- ポイント: スマホでスキャンできることを強調

### 3. n8n設定（8枚）

#### 3-1. n8n Cloudアカウント作成
- URL: https://n8n.io/cloud/
- 撮影内容: サインアップ画面
- ポイント: Free tierの説明

#### 3-2. 新規ワークフロー作成
- 撮影内容: 「Create new workflow」ボタン
- ポイント: 名前「プロンプト管理」

#### 3-3. ワークフローインポート
- 撮影内容: 右上メニュー → Import from File → workflow.json選択
- ポイント: インポート成功画面

#### 3-4. Webhook URL取得
- 撮影内容: Webhookノードをクリック → Production URL表示
- ポイント: URLをコピーボタンを強調

#### 3-5. LINE Webhook URL設定
- 撮影内容: LINE Developers → Webhook URL貼り付け → 「Verify」ボタン
- ポイント: 成功メッセージ表示

#### 3-6. Notion認証情報設定
- 撮影内容: n8n Credentials → Notion API → API Key入力
- ポイント: Database IDも入力

#### 3-7. LINE認証情報設定
- 撮影内容: n8n Credentials → LINE API → Channel Access Token/Secret入力
- ポイント: 2つの認証情報を入力

#### 3-8. ワークフロー有効化
- 撮影内容: 右上「Active」トグルをON
- ポイント: 緑色になったことを強調

### 4. 使用例（5枚）

#### 4-1. プロンプト送信
- 撮影内容: LINEアプリでメッセージ送信
- テキスト例:
```
プロンプト: あなたは経験豊富なマーケティングコンサルタントです。中小企業向けのSNS戦略を10個提案してください。
```

#### 4-2. 保存完了通知
- 撮影内容: LINEボットからの返信
- 表示内容:
```
✅ プロンプトを保存しました！

カテゴリ: マーケティング
タグ: マーケティング

Notionで確認できます。
```

#### 4-3. Notionで確認
- 撮影内容: Notionデータベースに保存されたプロンプト
- ポイント: カテゴリ・タグが自動付与されている

#### 4-4. 検索実行
- 撮影内容: LINEで「検索 マーケティング」送信 → 検索結果返信
- 表示内容:
```
🔍 検索結果: 3件

1. [マーケティング]
あなたは経験豊富なマーケティングコンサル...

2. [マーケティング]
SNS広告のROIを最大化するための...
```

#### 4-5. 一覧表示
- 撮影内容: LINEで「一覧」送信 → 最新10件表示
- ポイント: カテゴリ別に整理されている

### 5. 完成イメージ（3枚）

#### 5-1. システム全体図
- 撮影内容: 概念図（手書きまたはFigma）
```
[スマホ(LINE)] → [n8n] → [Notion] → [PC/スマホ同期]
```

#### 5-2. Notionダッシュボード
- 撮影内容: カテゴリ別ビュー・タグフィルタ・検索機能を活用
- ポイント: 100件以上のプロンプトが整理されている様子

#### 5-3. 実際の活用シーン
- 撮影内容: スマホでLINE操作 → PCでNotion確認の並列画面
- ポイント: シームレスな同期を強調

## 🎨 スクリーンショット撮影のコツ

### 全体ルール
- **解像度**: 最低1920x1080（Retina推奨）
- **圧縮**: TinyPNG等で最適化（100KB以下目標）
- **フォーマット**: PNG（UI）、JPEG（写真）
- **モザイク**: 認証情報・個人情報は必ずモザイク処理
- **矢印・強調**: Skitch、Annotate等で重要箇所を赤枠

### 画面分割撮影（スマホ+PC並列）
```
┌─────────────┬─────────────┐
│             │             │
│   スマホ    │     PC      │
│  (LINE)     │  (Notion)   │
│             │             │
└─────────────┴─────────────┘
```
- ツール: OBS Studio、Snagit
- ポイント: 同時操作感を演出

### GIF動画（オプション）
- 5秒以内の短いアニメーション
- 例: LINE送信 → Notion保存 → 通知返信の流れ
- ツール: ScreenToGif、LICEcap
- サイズ: 2MB以下

## 📋 撮影チェックリスト

- [ ] Notion設定（5枚）
- [ ] LINE Bot設定（6枚）
- [ ] n8n設定（8枚）
- [ ] 使用例（5枚）
- [ ] 完成イメージ（3枚）
- [ ] 全画像モザイク処理済み
- [ ] 全画像最適化済み（100KB以下）
- [ ] 矢印・強調追加済み
- [ ] GIF動画（オプション）

## 🚀 note記事への埋め込み

### 画像配置例
```markdown
## Notion設定（5分）

![Notionアカウント作成](images/01-notion-signup.png)

1. [Notion](https://www.notion.so/)でアカウント作成
2. 「Continue with Google」をクリック

![データベース作成](images/02-notion-database.png)

3. 新規ページ作成 → `/database` 入力
```

### GIF埋め込み
```markdown
実際の動作はこちら：

![プロンプト自動保存デモ](images/demo-save-prompt.gif)

LINEで送信すると即座にNotionに保存されます！
```

---

**最終更新**: 2025-11-16
