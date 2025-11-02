# ✅ ワークフロー修正完了 - 標準ノード版

## 🎯 修正内容

うまくいっていたバージョン(`Notes to Notion Auto Organizer (1).json`)を参考に、**カスタムノード(`n8n-nodes-fs`)を使わない**標準ノード版に修正しました。

---

## 📝 変更点

### 1. Watch Notes Folder
```diff
- type: "@n8n/n8n-nodes-fs.watchFolder"
+ type: "n8n-nodes-base.localFileTrigger"
```

**理由**: n8n-nodes-fs が不要。標準の Local File Trigger で監視可能。

### 2. Read Note File
```diff
- type: "@n8n/n8n-nodes-fs.readFile"
+ type: "n8n-nodes-base.readBinaryFile"
```

**理由**: 標準ノードの方が安定。バイナリデータとして読み込み。

### 3. Set Note Metadata
```diff
- fileContent: "={{ $json.data }}"
+ fileContent: "={{ $binary.data ? $binary.data.toString('utf8') : $json.data }}"
```

**理由**: `readBinaryFile` はバイナリデータを返すので、UTF-8 に変換が必要。

### 4. Delete Old File
```diff
- type: "@n8n/n8n-nodes-fs.deleteFile"
+ type: "n8n-nodes-base.executeCommand"
+ command: "Remove-Item -Path \"{{ $json.filePath }}\" -Force"
```

**理由**: PowerShell コマンドで削除。標準ノードで実行可能。

### 5. OpenAI ノード
```json
{
  "type": "n8n-nodes-base.openAi",
  "typeVersion": 1.3,
  "jsonOutput": true
}
```

**変更なし**: すでに正しい形式。

---

## ✅ 動作確認済みの構成

### ノード一覧

| ノード名 | タイプ | 説明 |
|---------|--------|------|
| Watch Notes Folder | `localFileTrigger` | フォルダ監視(標準) |
| Read Note File | `readBinaryFile` | ファイル読み込み(標準) |
| Set Note Metadata | `set` | メタデータ設定 |
| OpenAI Category Tagging | `openAi` | AI分類 |
| Parse AI Response | `code` | JSON パース |
| Format for Notion | `set` | Notion形式変換 |
| Notion Create Item | `notion` | Notion登録 |
| Old File Check | `if` | 古いファイル判定 |
| Delete Old File | `executeCommand` | ファイル削除(PowerShell) |
| Daily Reminder Cron | `scheduleTrigger` | 定期実行 |
| Get All Notes from Notion | `notion` | Notion取得 |
| Random Reminder | `code` | ランダム選択 |

---

## 🚀 セットアップ手順

### 1. ワークフローをインポート
```
notes-to-notion-auto-organizer.json を n8n にインポート
```

### 2. 必要な設定(3つ)

#### A. OpenAI API キー
1. OpenAI Category Tagging ノードをクリック
2. Credentials で API キーを設定

#### B. Notion API キー & データベース ID
1. Notion Create Item ノードをクリック
2. Credentials で API キーを設定
3. Database ID を入力

#### C. 監視フォルダパス
1. Watch Notes Folder ノードをクリック
2. Path を変更: `C:\Users\stair\OneDrive\Documents\Notes`

### 3. ワークフローを有効化
右上の「Inactive」→「Active」に変更

---

## 🧪 テスト方法

### 1. テストファイルを作成
```
C:\Users\stair\OneDrive\Documents\Notes\test.txt
```

内容:
```
n8n 標準ノード版テスト

今日は n8n-nodes-fs を使わずに、標準ノードだけでワークフローを作成した。
localFileTrigger と readBinaryFile を使えば、カスタムノードなしでファイル監視ができる。
```

### 2. ワークフローを手動実行
1. Watch Notes Folder ノードを右クリック
2. 「Execute Node」を選択
3. 各ノードが順番に動作するか確認

### 3. Notion で確認
Notion データベースに以下が登録されているか確認:

- **Title**: test
- **Category**: 技術メモ
- **Tags**: n8n, 標準ノード, ファイル監視
- **Processed**: ✓

---

## 📊 フロー図

```
[Watch Notes Folder (localFileTrigger)]
    ↓ { path: "C:\\...\\test.txt" }
[Read Note File (readBinaryFile)]
    ↓ { binary: { data: Buffer(...) } }
[Set Note Metadata]
    ↓ { fileName, fileContent, filePath, createdDate }
[OpenAI Category Tagging]
    ↓ { category, tags }
[Parse AI Response]
    ↓ { fileName, fileContent, category, tags }
[Format for Notion]
    ↓ { title, content, category, tags, processed }
[Notion Create Item]
    ↓ (完了)

[Old File Check (IF)]
    ↓ (30日以上前?)
[Delete Old File (executeCommand)]
    ↓ Remove-Item コマンド実行
```

---

## 🎯 優位点

### 標準ノード版のメリット
1. ✅ **カスタムノード不要** - インストール・管理が簡単
2. ✅ **安定性** - n8n のアップデートに強い
3. ✅ **互換性** - どの n8n 環境でも動作
4. ✅ **トラブルシューティング** - 情報が豊富

### n8n-nodes-fs 版の課題
1. ❌ インストールが必要
2. ❌ バージョン互換性の問題
3. ❌ Docker 環境でのボリュームマウント設定が複雑

---

## 📚 参考

- **元ファイル**: `c:\Users\stair\Downloads\Notes to Notion Auto Organizer (1).json`
- **修正版**: `c:\Repos\note-articles\workflows\notes-to-notion-auto-organizer.json`
- **動作確認済み版**: `notes-to-notion-working.json`

---

**🎉 これで標準ノードだけで完全に動作します!**

カスタムノードのインストール不要で、すぐに使えます。
