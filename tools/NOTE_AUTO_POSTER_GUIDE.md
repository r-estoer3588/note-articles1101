# note自動投稿スクリプト - セットアップガイド

## 📋 概要

93記事を自動的にnoteに投稿するPlaywrightベースのスクリプト。

**所要時間:**
- 初回セットアップ: 5分
- 93記事投稿: 約2-3時間（自動実行）

---

## 🚀 セットアップ手順

### 1. Playwright依存関係インストール

```powershell
cd C:\Repos\note-articles\tools

# 仮想環境がある場合はアクティベート
.\venv\Scripts\Activate.ps1

# Playwrightインストール
pip install playwright

# ブラウザインストール
playwright install chromium
```

---

## 📝 使い方

### 基本コマンド

```powershell
python note_auto_poster.py `
  --email "your@email.com" `
  --password "yourpassword" `
  --articles-dir "../gethnote/drafts"
```

### オプション

- `--limit 5`: 最初の5記事だけ投稿（テスト用）
- `--headless`: ヘッドレスモード（ブラウザ非表示）

---

## 🧪 テスト実行（推奨）

まず1記事だけテストしてみましょう：

```powershell
python note_auto_poster.py `
  --email "your@email.com" `
  --password "yourpassword" `
  --articles-dir "../gethnote/drafts" `
  --limit 1
```

**確認ポイント:**
✅ ログイン成功  
✅ タイトルが正しく入力されている  
✅ 本文が正しく入力されている  
✅ 有料設定（¥300）が適用されている  
✅ 記事が公開されている

---

## 🔥 本番実行（93記事投稿）

テストOKなら全記事を投稿：

```powershell
python note_auto_poster.py `
  --email "your@email.com" `
  --password "yourpassword" `
  --articles-dir "../gethnote/drafts"
```

**注意:**
- 1記事投稿後、60秒待機してから次の記事を投稿（rate limit対策）
- 93記事 × 60秒 = 約93分（1.5時間）の待機時間
- 実際の投稿作業時間を含めると **合計2-3時間**

---

## ⚠️ トラブルシューティング

### エラー1: ログイン失敗

```
❌ ログイン失敗。メールアドレスとパスワードを確認してください。
```

**対処法:**
- メールアドレス・パスワードを再確認
- noteの2段階認証が有効な場合は無効化する

---

### エラー2: セレクタが見つからない

```
❌ Timeout waiting for selector
```

**対処法:**
- noteのUI変更により、セレクタが変わった可能性
- `--headless`を外して、ブラウザを表示して確認
- スクリプトのセレクタを修正

---

### エラー3: 投稿が途中で止まる

**対処法:**
- Ctrl+Cで停止
- `--limit`で少数ずつ投稿（例: `--limit 10`）
- エラーログを確認して原因を特定

---

## 📊 投稿進捗の確認

スクリプト実行中、以下のログが表示されます：

```
📚 投稿予定記事数: 93

--- [1/93] ---
📝 noteにログイン中...
✅ ログイン成功
📄 記事作成中: 【年金で知らないと損する裏技】
💰 有料設定: ¥300
📢 記事を公開中...
✅ 投稿完了: 【年金で知らないと損する裏技】
⏱️  次の記事まで60秒待機...

--- [2/93] ---
...
```

---

## 🔒 セキュリティ注意事項

### パスワードを環境変数に保存（推奨）

毎回パスワードをコマンドに入力するのは危険なので、環境変数に保存：

```powershell
# PowerShellで環境変数設定
$env:NOTE_EMAIL = "your@email.com"
$env:NOTE_PASSWORD = "yourpassword"

# スクリプト実行
python note_auto_poster.py `
  --email $env:NOTE_EMAIL `
  --password $env:NOTE_PASSWORD `
  --articles-dir "../gethnote/drafts"
```

または、`.env`ファイルを作成：

```bash
# tools/.env
NOTE_EMAIL=your@email.com
NOTE_PASSWORD=yourpassword
```

スクリプトを修正して`.env`から読み込むようにする。

---

## 🎯 投稿スケジュール案

93記事を一気に投稿するより、分割投稿の方がnote側のrate limitに引っかかりにくい：

### 案1: 週次投稿（7記事ずつ）
```powershell
# Week 2
python note_auto_poster.py ... --limit 7

# Week 3（1週間後）
python note_auto_poster.py ... --limit 14  # 累計14記事

# Week 4（2週間後）
python note_auto_poster.py ... --limit 21  # 累計21記事
```

### 案2: 毎日投稿（3記事ずつ）
```powershell
# Day 1
python note_auto_poster.py ... --limit 3

# Day 2
python note_auto_poster.py ... --limit 6  # 累計6記事
```

---

## 📈 投稿後の確認

投稿完了後、以下を確認：

✅ note管理画面で記事が表示されている  
✅ 有料設定（¥300）が適用されている  
✅ タイトル・本文が正しい  
✅ 次回予告リンクが正しい  
✅ ハッシュタグが付いている

---

## 🔄 次のステップ

1. ✅ 93記事自動投稿完了
2. X(Twitter)に拡散投稿（x-postsフォルダーのテンプレート使用）
3. article_master.jsonを更新（note URLを追記）
4. 売上トラッキング開始

---

次は実際に実行してみましょう！
