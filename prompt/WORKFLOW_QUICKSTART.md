# 🚀 一気通貫ワークフロー - クイックスタート

note記事のリライトから保存まで、たった1コマンドで完結！

## 📋 事前準備（初回のみ）

### 1. フォルダ構成を確認

```
note-articles/
├── drafts/          # リライト後の記事が保存される
├── articles/        # 投稿完了後、ここに移動
└── prompt/
    ├── run-prompt.ps1
    ├── save-note-article.ps1
    └── note-workflow.ps1
```

### 2. ChatGPTアカウント

- https://chat.openai.com/ にログイン済み

## 🎯 使い方（3パターン）

### パターン1: ファイルから読み込む（推奨）

```powershell
# 記事ファイルを指定
.\note-workflow.ps1 -ArticleFile C:\path\to\draft.txt -AutoOpen

# 実行後の流れ:
# 1. プロンプト + 記事本文がクリップボードにコピーされる
# 2. ChatGPTを開く
# 3. Ctrl+V で貼り付け → Enter
# 4. 出力をすべてコピー (Ctrl+A → Ctrl+C)
# 5. ターミナルに戻って Enter
# 6. 自動的にMarkdownファイルが保存される
# 7. VS Codeで開かれる
```

### パターン2: クリップボードから

```powershell
# 記事をコピーしてから実行
Get-Clipboard | .\note-workflow.ps1 -AutoOpen
```

### パターン3: 直接テキストを渡す

```powershell
.\note-workflow.ps1 @'
AIで書いたnote、なんか、つまらない。
読んでも心動かない。なぜなのか。
'@ -AutoOpen
```

## 📝 実行例

### 例1: 基本的な使い方

```powershell
PS> .\note-workflow.ps1 -ArticleFile draft.txt

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   🚀 Note Workflow Automation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 ファイルから記事を読み込んでいます: draft.txt
✅ 読み込み完了（1234文字）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 1: プロンプト準備
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔄 note_prompt.txt + 記事本文をクリップボードにコピー中...
✅ クリップボードにコピーしました: 📝 記事構成設計プロンプト

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏸️  手動操作が必要です
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

次の手順を実行してください:

1️⃣  ChatGPTを開く: https://chat.openai.com/
2️⃣  Ctrl+V でプロンプトを貼り付け
3️⃣  Enter で実行
4️⃣  出力された【全文リライト案】をすべてコピー (Ctrl+A → Ctrl+C)
5️⃣  このウィンドウに戻って Enter を押す

準備ができたら Enter キーを押してください...
```

### （Enter を押した後）

```powershell
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 2: ChatGPT出力を取得
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 クリップボードからChatGPTの出力を取得しています...
✅ ChatGPTの出力を取得しました（5678文字）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 3: Markdownファイルに保存
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 タイトルを自動抽出: AI動画で月10万稼ぐ方法

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Markdownファイルを保存しました!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 ファイル名: 20251103_143000_AI動画で月10万稼ぐ方法.md
📂 保存場所: C:\Repos\note-articles\drafts\20251103_143000_AI動画で月10万稼ぐ方法.md
📏 文字数: 5678 文字

💡 相対パス: drafts\20251103_143000_AI動画で月10万稼ぐ方法.md

📝 ファイルを開いています...
✅ VS Codeで開きました

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎉 すべての処理が完了しました!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 📂 保存されたファイルの例

**ファイル名:** `20251103_143000_AI動画で月10万稼ぐ方法.md`

**場所:** `note-articles/drafts/`

**内容:**
```markdown
---
title: AI動画で月10万稼ぐ方法
created: 2025-11-03 14:30:00
source: ChatGPT (note-articles prompt)
---

# AI動画で月10万稼ぐ方法

（リライトされた本文がここに入る）

---

## メタ情報
- 作成日時: 2025年11月03日 14:30
- 生成元: note_prompt.txt
- ステータス: 下書き

## 次のアクション
- [ ] タイトルの最終確認
- [ ] 本文の誤字脱字チェック
- [ ] noteに投稿
- [ ] SNSでシェア
```

## 🎯 次のステップ

### 1. 記事を確認・編集

```powershell
# VS Codeで開く（自動的に開かれている場合はスキップ）
code drafts\20251103_143000_AI動画で月10万稼ぐ方法.md
```

### 2. noteに投稿

1. https://note.com/new を開く
2. Markdownファイルの内容をコピー&ペースト
3. プレビューを確認
4. 投稿ボタンをクリック

### 3. 投稿完了後、ファイルを移動

```powershell
# drafts → articles に移動
Move-Item "drafts\20251103_143000_AI動画で月10万稼ぐ方法.md" "articles\"
```

## 💡 便利なオプション

### タイトルを手動指定

```powershell
.\note-workflow.ps1 -ArticleFile draft.txt -Title "カスタムタイトル" -AutoOpen
```

### 保存後に自動的に開かない

```powershell
.\note-workflow.ps1 -ArticleFile draft.txt
# -AutoOpen を付けない
```

## 🔧 トラブルシューティング

### Q: クリップボードが空だと言われる

**A:** 記事をコピーしてから実行してください
```powershell
Get-Content draft.txt | Set-Clipboard
.\note-workflow.ps1
```

### Q: タイトルが正しく抽出されない

**A:** 手動でタイトルを指定してください
```powershell
.\note-workflow.ps1 -ArticleFile draft.txt -Title "正しいタイトル"
```

### Q: VS Codeで開かれない

**A:** `code` コマンドが使えるか確認
```powershell
# パスが通っているか確認
Get-Command code

# 通っていない場合、手動で開く
Start-Process "drafts\ファイル名.md"
```

## 🎉 完全自動化の未来

現在は ChatGPT へのコピペが手動ですが、将来的には:

- ChatGPT API連携で完全自動化
- note API連携で自動投稿
- GitHub Actions で定期実行

など、さらなる自動化も可能です！

## 📞 サポート

問題が発生した場合:
1. `.\note-workflow.ps1` の出力メッセージを確認
2. `drafts` フォルダにファイルが保存されているか確認
3. PowerShellのバージョンを確認（5.1以上推奨）

**さあ、一気通貫ワークフローで効率的に記事を量産しよう！**
