# 🎯 n8n Notes Organizer - 簡単スタートガイド

## 💡 何ができる?

ノートファイルを `C:\Users\stair\OneDrive\Documents\Notes` に置くだけで:
1. ✅ 自動的にAIが内容を分析
2. ✅ カテゴリとタグを自動生成
3. ✅ Notionに自動登録

**一度セットアップすれば、二度と設定不要!**

---

## 🚀 初回セットアップ(一度だけ!)

### Step 1: n8nを起動

```powershell
cd C:\Repos\note-articles\workflows
.\start-n8n.ps1
```

ブラウザで http://localhost:5678 が開きます

### Step 2: ワークフローをインポート

1. **n8n UIの右上メニュー** → **Import from File**
2. **`notes-to-notion-auto-organizer.json`** を選択
3. **Import** をクリック

### Step 3: APIキーを設定(3つだけ!)

#### 1️⃣ OpenAI API キー

- **OpenAI Category Tagging ノードをクリック**
- **Credentials** → **Create New**
- API キーを貼り付け → 保存

#### 2️⃣ Notion API キー

1. https://www.notion.so/my-integrations で Integration作成
2. **Internal Integration Token** をコピー
3. **Notion Create Item ノードをクリック**
4. **Credentials** → **Create New**
5. API キーを貼り付け

#### 3️⃣ Notion データベース ID

1. Notionでデータベースを開く
2. URLの `https://notion.so/xxxxx?v=yyyyy` の **xxxxx** をコピー
3. **Notion Create Item ノード** → **Database ID** に貼り付け

### Step 4: ワークフローをActiveに

- 右上の **トグルスイッチ** を **ON** にする

---

## 🎉 完成!以降は何もしなくていい

```powershell
# PCを起動したら、これだけ実行
.\start-n8n.ps1

# 停止するとき
.\stop-n8n.ps1
```

設定は**永久に保存**されます!

---

## 📝 日常的な使い方

### ノートを追加

```powershell
# メモ帳でファイルを作成
notepad "C:\Users\stair\OneDrive\Documents\Notes\今日の学び.txt"

# 内容を書いて保存
# → 自動的にNotionに登録される!
```

### Notionで確認

- カテゴリ、タグが自動的に付与されている
- ファイル内容がそのまま保存されている

---

## 🔧 よくある質問

### Q: 毎回APIキーを設定しないといけない?

**A: いいえ!** 一度設定すれば永久保存されます。

### Q: PCを再起動したら?

**A: `.\start-n8n.ps1` を実行するだけ!** 設定はそのままです。

### Q: Docker Desktopを再インストールしたら?

**A: `docker volume ls` で `n8n_data` があれば設定は残ってます。**

なければ、初回セットアップをやり直してください(APIキー設定が必要)。

### Q: ワークフローをカスタマイズしたい

**A: n8n UI上で直接編集できます。** 変更は自動保存されます。

### Q: バックアップは?

```powershell
# 設定をバックアップ
docker run --rm -v n8n_data:/data -v ${PWD}:/backup alpine tar czf /backup/n8n_backup.tar.gz -C /data .

# 復元
docker run --rm -v n8n_data:/data -v ${PWD}:/backup alpine tar xzf /backup/n8n_backup.tar.gz -C /data
```

---

## 📚 詳細ドキュメント

- **永続化の仕組み**: `PERSISTENT_SETUP.md`
- **カスタマイズ方法**: `CUSTOMIZATION.md`
- **トラブルシューティング**: `TROUBLESHOOTING.md`

---

## ✅ これだけ覚えればOK

```powershell
# 起動
.\start-n8n.ps1

# 停止(設定は残る)
.\stop-n8n.ps1

# ノートを追加するだけ
# → 自動でNotionに登録!
```

**🎉 以上!超簡単!**
