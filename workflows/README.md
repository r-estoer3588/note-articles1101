# Notes to Notion Auto Organizer

ローカルフォルダに置いたノートファイルを自動で読み込み、OpenAI で分類して Notion に登録する n8n ワークフローです。

---

## � **今すぐ始める → [`HOW_TO_USE.md`](HOW_TO_USE.md)**

**一度設定すれば、二度と設定不要!**

---

## �📂 ファイル一覧

### ⭐ 推奨ドキュメント
- **HOW_TO_USE.md** - 🔥**最も簡単な使い方ガイド(まずこれを読む!)**
- **docker-compose.yml** - n8n環境の永続化設定
- **PERSISTENT_SETUP.md** - 詳細な永続化セットアップガイド
- **start-n8n.ps1** - n8n起動スクリプト(設定は自動保存)
- **stop-n8n.ps1** - n8n停止スクリプト

### ワークフローファイル
- **notes-to-notion-auto-organizer.json** - n8n ワークフロー本体(インポート用)
- **CUSTOMIZATION.md** - OpenAI プロンプトとフロー拡張のカスタマイズガイド

### 従来のドキュメント(非推奨)
- ~~**QUICKSTART.md** - 従来の5分クイックスタート(毎回設定が必要)~~
- ~~**SETUP_GUIDE.md** - 従来の詳細セットアップ(毎回設定が必要)~~

---

## 🎯 どのファイルを読めばいい?

| 状況 | 読むべきファイル |
|------|------------------|
| 🔰 **初めて使う** | **[`HOW_TO_USE.md`](HOW_TO_USE.md)** ← まずこれ! |
| 🔧 永続化の詳細を知りたい | [`PERSISTENT_SETUP.md`](PERSISTENT_SETUP.md) |
| 🎨 AIプロンプトをカスタマイズ | [`CUSTOMIZATION.md`](CUSTOMIZATION.md) |
| 🐛 トラブルが発生した | [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md) |

---

## 📋 機能

### メインフロー
1. **ファイル監視**: `C:\Users\stair\OneDrive\Documents\Notes` フォルダを監視
2. **自動読み込み**: 新規ファイルが追加されたら自動で内容を読み取り
3. **AI 分類**: OpenAI (gpt-4o-mini) でカテゴリとタグを自動生成
4. **Notion 登録**: 分類結果とともに Notion データベースに保存

### サブ機能
- **古いファイル削除**: 30日以上前のファイルを自動削除
- **定期リマインド**: 毎日9時にランダムなノートを選択(通知ノードに接続可能)

---

## 🚀 セットアップ手順

### ⭐ 推奨: 永久保存方式

**`PERSISTENT_SETUP.md` を参照してください**

一度セットアップすれば、以降は何もする必要がありません:
- ✅ Docker起動だけでOK
- ✅ 設定は全部保存される
- ✅ 再起動しても消えない
- ✅ APIキーを毎回入れ直す必要なし

```powershell
# workflows/ ディレクトリで実行
docker-compose up -d

# ブラウザで http://localhost:5678 を開く
# (初回のみワークフローをインポート)
```

---

### 従来の方式(非推奨 - 毎回セットアップが必要)

<details>
<summary>クリックして展開</summary>

### 1. n8n にワークフローをインポート

```bash
# Docker で n8n を起動している場合
# n8n UI から「Import from File」を選択し、
# notes-to-notion-auto-organizer.json をアップロード
```

### 2. 必要な認証情報を設定

#### OpenAI API
- **OpenAI Category Tagging** ノードで使用
- OpenAI API キーを登録(n8n の Credentials 画面から)

#### Notion API
- **Notion Create Item** ノードと **Get All Notes from Notion** ノードで使用
- Notion Integration を作成し、API キーを取得
- データベース ID を確認して設定

#### File System(オプション)
- **Delete Old File** ノードで使用
- n8n-nodes-fs がインストール済みであれば、認証情報を設定

### 3. 監視フォルダパスを変更

**Watch Notes Folder** ノードの `path` パラメータを環境に合わせて変更:

```json
"path": "C:\\Users\\stair\\OneDrive\\Documents\\Notes"
```

### 4. Notion データベースのプロパティを確認

Notion データベースに以下のプロパティが必要です:

- **Title**: タイトル(必須)
- **Category**: テキスト
- **Tags**: マルチセレクト
- **Processed**: チェックボックス

### 5. ワークフローを有効化

n8n UI でワークフローを「Active」に変更すれば、自動で動作します。

</details>

---

## 🎯 使い方

1. 監視フォルダにテキストファイルを追加
2. 自動でファイルが読み込まれ、AI が内容を分析
3. カテゴリとタグが付与されて Notion に登録
4. 30日後に元のファイルが自動削除(オプション)

---

## 📊 フロー図

```
[Watch Notes Folder]
    ↓
[Read Note File]  ← ★ここの接続がポイント!
    ↓
[Set Note Metadata] ─┬→ [OpenAI Category Tagging]
                     │       ↓
                     │   [Parse AI Response]
                     │       ↓
                     │   [Format for Notion]
                     │       ↓
                     │   [Notion Create Item]
                     │
                     └→ [Old File Check (IF)]
                             ↓ (TRUE)
                         [Delete Old File]

[Daily Reminder Cron]
    ↓
[Get All Notes from Notion]
    ↓
[Random Reminder]
    ↓
(ここから Slack/Discord/Email に接続可能)
```

---

## ⚙️ カスタマイズ例

### AI プロンプトの調整

**OpenAI Category Tagging** ノードの `messages` を編集して、分類ルールを変更できます:

```json
{
  "role": "system",
  "content": "日本語のノートを分類してください。カテゴリは「技術メモ」「読書メモ」「アイデア」のいずれかにしてください。"
}
```

### 古いファイルの保存期間変更

**Old File Check** ノードの条件を変更:

```javascript
// 30日 → 90日に変更
{{ $now.minus({ days: 90 }).toMillis() }}
```

### リマインド時刻の変更

**Daily Reminder Cron** ノードの `interval` を変更:

```json
{
  "rule": {
    "interval": [
      {
        "field": "hours",
        "hoursInterval": 24,
        "triggerAtHour": 9  // 毎日9時
      }
    ]
  }
}
```

---

## 🔧 トラブルシューティング

### ファイルが読み込まれない
- Watch Notes Folder のパスが正しいか確認
- Docker コンテナからフォルダにアクセスできるか確認(ボリュームマウント設定)

### OpenAI でエラーが出る
- API キーが正しく設定されているか確認
- OpenAI のクォータ(利用上限)を確認

### Notion に登録されない
- データベース ID が正しいか確認
- Notion Integration がデータベースに接続されているか確認
- プロパティ名(Category, Tags など)が一致しているか確認

### 古いファイルが削除されない
- n8n-nodes-fs がインストールされているか確認
- File System の認証情報が設定されているか確認
- Docker コンテナに削除権限があるか確認

---

## 📝 ライセンス

このワークフローは自由に改変・配布できます。

## 🙋 サポート

問題が発生した場合は、n8n のコミュニティフォーラムや Discord で質問してください。
