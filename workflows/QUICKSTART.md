# 🚀 Quick Start - 5分で始める Notes to Notion

## 📦 インポート

1. n8n UI を開く
2. 右上のメニューから **「Import from File」** を選択
3. `notes-to-notion-auto-organizer.json` をアップロード

---

## 🔌 接続の直し方(Watch Notes Folder → Read Note File)

### 現状: 接続されていない状態

```
[Watch Notes Folder]     [Read Note File]
         ●                      ●
    (右端のドット)          (左端のドット)
```

### 手順

1. **Watch Notes Folder の右端の●をクリック**
2. **マウスを Read Note File の左端の●までドラッグ**
3. **ドロップすると線がつながる**

```
[Watch Notes Folder] ────→ [Read Note File]
```

### 確認方法

- 線が表示されていれば OK
- または JSON で確認:

```json
"connections": {
  "Watch Notes Folder": {
    "main": [[{"node": "Read Note File"}]]
  }
}
```

---

## ⚙️ 必須設定(3つだけ)

### 1. OpenAI API キー

1. **OpenAI Category Tagging ノードをクリック**
2. **Credentials** セクションで **「Create New」**
3. API キーを入力して保存

### 2. Notion API キー & データベース ID

#### Notion Integration を作成
1. https://www.notion.so/my-integrations にアクセス
2. **「New integration」** をクリック
3. 名前を `n8n-notes-organizer` にして作成
4. **Internal Integration Token** をコピー

#### データベース ID を取得
1. Notion でデータベースを開く
2. URL をコピー: `https://notion.so/xxxxx?v=yyyyy`
3. `xxxxx` の部分がデータベース ID

#### n8n に設定
1. **Notion Create Item ノードをクリック**
2. **Credentials** で **「Create New」**
3. API キーを貼り付け
4. **Database ID** に `xxxxx` を貼り付け

### 3. 監視フォルダパスを変更

**Watch Notes Folder ノードをクリック**

```json
{
  "path": "C:\\Users\\stair\\OneDrive\\Documents\\Notes"
}
```

自分の環境に合わせて変更(バックスラッシュは2つ `\\`)

---

## 🧪 テスト実行

### 1. テストファイルを作成

`C:\Users\stair\OneDrive\Documents\Notes\test.txt` を作成:

```
n8n の自動化テスト

今日は n8n で Notes フォルダを監視して、自動的に Notion に登録する仕組みを作った。
OpenAI でカテゴリとタグを自動生成するのが便利。
```

### 2. ワークフローを実行

1. **Watch Notes Folder ノードを右クリック**
2. **「Execute Node」** を選択
3. 各ノードが順番に実行されるのを確認

### 3. Notion で確認

Notion データベースに以下のようなアイテムが追加されます:

- **Title**: test
- **Category**: 技術メモ
- **Tags**: n8n, 自動化, Notion
- **Processed**: ✓

---

## 🎯 フロー全体像

```
┌─────────────────────┐
│Watch Notes Folder   │ ← フォルダ監視(トリガー)
└──────┬──────────────┘
       │ { path: "C:\\...\\test.txt" }
       ↓
┌─────────────────────┐
│Read Note File       │ ← ファイル内容を読み込む
└──────┬──────────────┘
       │ { path, data: "ファイル内容" }
       ↓
┌─────────────────────┐
│Set Note Metadata    │ ← ファイル名や作成日時を追加
└──────┬──────────────┘
       │ { fileName, fileContent, filePath, createdDate }
       ├──────────────────────┐
       │                      │
       ↓                      ↓
┌─────────────────────┐  ┌─────────────────────┐
│OpenAI Category      │  │Old File Check (IF)  │
│Tagging              │  └──────┬──────────────┘
└──────┬──────────────┘         │ (30日以上前?)
       │ AI分析                  ↓ (TRUE)
       ↓                  ┌─────────────────────┐
┌─────────────────────┐  │Delete Old File      │
│Parse AI Response    │  └─────────────────────┘
└──────┬──────────────┘
       │ { category, tags }
       ↓
┌─────────────────────┐
│Format for Notion    │ ← Notion形式に整形
└──────┬──────────────┘
       │ { title, content, category, tags, processed }
       ↓
┌─────────────────────┐
│Notion Create Item   │ ← Notionに登録
└─────────────────────┘


─── サブフロー: 定期リマインド ───

┌─────────────────────┐
│Daily Reminder Cron  │ ← 毎日9時に実行
└──────┬──────────────┘
       ↓
┌─────────────────────┐
│Get All Notes from   │ ← Notionから全ノート取得
│Notion               │
└──────┬──────────────┘
       ↓
┌─────────────────────┐
│Random Reminder      │ ← ランダムに1つ選択
└─────────────────────┘
       ↓
   (通知ノードに接続可能)
```

---

## 🔧 次のステップ

### 完成後にやること

1. **ワークフローを Active にする**
   - 右上のトグルを ON にすれば自動実行開始

2. **Docker のボリュームマウントを確認**
   ```yaml
   # docker-compose.yml
   volumes:
     - C:\Users\stair\OneDrive\Documents\Notes:/notes
   ```

3. **リマインド通知を追加(オプション)**
   - Random Reminder の後に Discord/Slack ノードを追加

---

## ❓ トラブルシューティング

| 問題 | 原因 | 解決方法 |
|------|------|----------|
| ファイルが読み込まれない | 接続されていない | Watch → Read の接続を確認 |
| OpenAI エラー | API キー未設定 | Credentials を確認 |
| Notion に登録されない | データベース ID 間違い | URL から再確認 |
| 古いファイルが削除されない | n8n-nodes-fs 未インストール | `npm install n8n-nodes-fs` |

---

## 📚 詳細ドキュメント

- **基本的な使い方**: `README.md`
- **詳細なセットアップ**: `SETUP_GUIDE.md`
- **ワークフロー JSON**: `notes-to-notion-auto-organizer.json`

---

**🎉 完成!**

これで Notes フォルダにファイルを追加するだけで、自動的に AI が分類して Notion に登録してくれます。
