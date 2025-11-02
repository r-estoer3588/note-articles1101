# ✅ 完成版ワークフロー - セットアップガイド

## 🎯 修正完了内容

1. ✅ **Watch Notes Folder のトリガー設定を追加**
   - Path: `C:\Users\stair\OneDrive\Documents\Notes`
   - Event: `add` (ファイル追加時にトリガー)

2. ✅ **OpenAI Category Tagging の設定を完成**
   - Model: gpt-4o-mini
   - Temperature: 0.3
   - JSON Output: true
   - プロンプト設定済み

3. ✅ **接続を修正**
   - Set Note Metadata → OpenAI Category Tagging (追加)
   - OpenAI Category Tagging → Parse AI Response (追加)

---

## 📊 完成フロー

```
[Watch Notes Folder] ← トリガー(ファイル追加時)
    ↓
[Read Note File] ← バイナリファイル読み込み
    ↓
[Set Note Metadata] ← fileName, fileContent, filePath, createdDate
    ↓ ↓
    │ └→ [Old File Check (IF)] → [Delete Old File]
    ↓
[OpenAI Category Tagging] ← AI分類
    ↓
[Parse AI Response] ← JSONパース
    ↓
[Format for Notion] ← Notion形式に変換
    ↓
[Notion Create Item] ← Notion登録


─── サブフロー: 定期リマインド ───

[Daily Reminder Cron] ← 毎時実行
    ↓
[Get All Notes from Notion] ← 全ノート取得
    ↓
[Random Reminder] ← ランダム選択
    ↓
(通知ノードに接続可能)
```

---

## 🚀 セットアップ手順

### 1. ワークフローをインポート

n8n UI で:
1. 右上のメニュー → **Import from File**
2. `notes-to-notion-auto-organizer.json` を選択
3. Import をクリック

### 2. 既に設定済みの項目

以下は既に設定されています:

✅ **Watch Notes Folder**
- Path: `C:\Users\stair\OneDrive\Documents\Notes`
- Event: ファイル追加時

✅ **OpenAI API**
- Credential ID: `LH7QbsEMB3R638C6`
- Model: gpt-4o-mini

✅ **Notion API**
- Credential ID: `gSF7MeWTgomzvBzA`
- Database ID: `29e1972f485180c89c68d77f1b82e39f`

### 3. 確認が必要な項目

念のため以下を確認してください:

#### A. 監視フォルダの存在確認
```powershell
Test-Path "C:\Users\stair\OneDrive\Documents\Notes"
# True が返ればOK
```

#### B. Notion データベースのプロパティ
Notion データベースに以下のプロパティがあるか確認:
- **Title** (タイトル - 必須)
- **Category** (テキスト)
- **Tags** (マルチセレクト)
- **Processed** (チェックボックス)

#### C. Get All Notes from Notion のデータベース ID
このノードだけ `YOUR_NOTION_DATABASE_ID` になっているので、修正が必要:
1. Get All Notes from Notion ノードをクリック
2. Database ID を `29e1972f485180c89c68d77f1b82e39f` に変更

---

## 🧪 テスト方法

### 1. 手動トリガーでテスト

最初は Watch Notes Folder を使わず、手動でテスト:

1. **Set Note Metadata ノードをクリック**
2. **「Execute Node」** を選択
3. 手動でテストデータを設定
4. 各ノードが順番に動作するか確認

### 2. ファイル追加でテスト

Watch Notes Folder が動作するかテスト:

```powershell
# テストファイルを作成
@"
n8n 自動化テスト

今日は Notes フォルダにファイルを追加するだけで、
自動的に OpenAI が分類して Notion に登録してくれる仕組みを作った。
便利すぎる!
"@ | Out-File "C:\Users\stair\OneDrive\Documents\Notes\test-$(Get-Date -Format 'yyyyMMdd-HHmmss').txt" -Encoding UTF8
```

### 3. Notion で確認

Notion データベースに以下が登録されているか確認:

- **Title**: test-20251102-123456
- **Category**: 技術メモ
- **Tags**: ["n8n", "自動化", "Notion"]
- **Processed**: ✓
- **Content**: ファイルの内容

---

## ⚙️ Watch Notes Folder のトリガー設定

### 現在の設定

```json
{
  "path": "C:\\Users\\stair\\OneDrive\\Documents\\Notes",
  "event": "add"
}
```

### 設定オプション

#### event の選択肢

| 値 | 説明 | おすすめ度 |
|----|------|-----------|
| `add` | ファイル追加時のみ | ⭐⭐⭐ (推奨) |
| `change` | ファイル変更時のみ | ⭐⭐ |
| `add,change` | 追加と変更の両方 | ⭐ (重複注意) |

**推奨**: `add` のみ
- ファイル編集時に何度も実行されるのを防ぐ
- 新規ノートだけを登録

#### その他のオプション

```json
{
  "path": "C:\\Users\\stair\\OneDrive\\Documents\\Notes",
  "event": "add",
  "options": {
    "includeSubfolders": false,  // サブフォルダを含めない
    "filePattern": "*.txt,*.md"  // .txt と .md のみ監視
  }
}
```

### トリガーの動作確認

1. **ワークフローを Active にする**
   - 右上の「Inactive」→「Active」に変更

2. **テストファイルを追加**
   ```powershell
   "テストノート" | Out-File "C:\Users\stair\OneDrive\Documents\Notes\trigger-test.txt" -Encoding UTF8
   ```

3. **Executions タブで確認**
   - 左メニューの「Executions」をクリック
   - 実行履歴が表示されればトリガー成功

---

## 🔧 トラブルシューティング

### トリガーが動かない

**原因1**: ワークフローが Inactive
- **解決**: 右上を「Active」に変更

**原因2**: n8n がフォルダにアクセスできない
- **解決**: n8n を管理者権限で実行

**原因3**: OneDrive の同期が遅い
- **解決**: ローカルフォルダ(`C:\Notes`)を使う

### OpenAI でエラー

**原因**: API キーの期限切れ
- **解決**: OpenAI のダッシュボードで確認

### Notion に登録されない

**原因**: プロパティ名が一致しない
- **解決**: Notion データベースのプロパティを確認
  - Category (大文字小文字を正確に)
  - Tags
  - Processed

---

## 📝 次のステップ

### オプション機能を追加

1. **Discord/Slack 通知**
   - Random Reminder の後に Discord ノードを追加

2. **タグの自動整理**
   - Parse AI Response で重複タグを削除

3. **画像の自動アップロード**
   - ファイルに画像リンクがあれば Notion に追加

---

## 🎉 完成!

これで **ファイルを追加するだけで自動的に AI が分類して Notion に登録**してくれます。

### 使い方

1. `C:\Users\stair\OneDrive\Documents\Notes` にファイルを追加
2. 自動で AI が分類
3. Notion に登録完了!

**トリガーは既に `add` (ファイル追加時)に設定済みです。**

ワークフローを Active にすれば、すぐに使えます!
