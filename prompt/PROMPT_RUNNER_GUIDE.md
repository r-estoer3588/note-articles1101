# 📚 Prompt Runner - 使い方ガイド

プロンプトをコマンドラインから簡単に実行できるツールです。

## 🚀 クイックスタート

### 📍 どこからでも実行可能!

以下の3つのどのディレクトリからでも実行できます:

**1. C:\Repos から実行**
```powershell
cd C:\Repos
.\run-prompt.ps1 -PromptType note -Action copy
```

**2. C:\Repos\note-articles から実行**
```powershell
cd C:\Repos\note-articles
.\run-prompt.ps1 -PromptType note -Action copy
```

**3. C:\Repos\note-articles\prompt から実行（推奨）**
```powershell
cd C:\Repos\note-articles\prompt
.\run-prompt.ps1 -PromptType note -Action copy
```

### 基本的な使い方

```powershell
# プロンプト一覧を表示
.\run-prompt.ps1 -PromptType all

# 記事構成設計プロンプトをクリップボードにコピー
.\run-prompt.ps1 -PromptType note -Action copy

# 商品設計プロンプトを表示
.\run-prompt.ps1 -PromptType product -Action show

# AI動画収益化プロンプトをエディタで開く
.\run-prompt.ps1 -PromptType video -Action open
```

## 📋 利用可能なプロンプト

| コマンド | プロンプト名 | 説明 |
|---------|------------|------|
| `note` | 📝 記事構成設計プロンプト | 読者が行動・購入・共感する記事構成を設計 |
| `product` | 🎯 商品設計フレームワーク | ChatGPT活用型の商品設計（ペルソナ100個→商品案→コピー生成） |
| `video` | 🎬 AI動画×収益化フレームワーク | AI動画生成からSNS集客、自動化までの完全ガイド |

## 🎯 アクション一覧

| アクション | 説明 |
|-----------|------|
| `show` | プロンプト内容をコンソールに表示 |
| `copy` | クリップボードにコピー（**デフォルト**） |
| `open` | デフォルトエディタ（VS Code優先）で開く |

## 💡 実用例

### 1. 記事を書く前に構成を設計したい

```powershell
# 記事構成プロンプトをコピー
.\run-prompt.ps1 -PromptType note -Action copy

# → ChatGPTに貼り付け
# → 記事本文を追加入力
# → 構成設計を受け取る
```

### 2. 商品のアイデアを練りたい

```powershell
# 商品設計プロンプトをコピー
.\run-prompt.ps1 -PromptType product -Action copy

# → ChatGPTに貼り付け
# → 業界名を入力（例：副業、婚活、英語学習）
# → ペルソナ100個→商品案10個を受け取る
```

### 3. AI動画で収益化したい

```powershell
# 動画収益化プロンプトをコピー
.\run-prompt.ps1 -PromptType video -Action copy

# → ChatGPTに貼り付け
# → 収益化方法5つ→SNS投稿文20本→自動化の仕組みを受け取る
```

### 4. 記事本文を直接渡してリライト

**方法1: ヒアドキュメント（@' '@）を使う**
```powershell
.\run-prompt.ps1 -PromptType note -Action copy @'
AIで書いたnote、なんか、つまらない。
読んでも心動かない。なぜなのか。

実は、AI×noteで難しいことがあるんよ。
ただAI使ってるだけだと「教育」ができない。
'@

# プロンプト + 記事本文がセットでコピーされる
# → ChatGPTに貼り付けるだけ!
```

**方法2: ファイルから読み込む**
```powershell
# article.txtの内容を記事本文として渡す
Get-Content article.txt -Raw | .\run-prompt.ps1 -PromptType note -Action copy

# または
.\run-prompt.ps1 -PromptType note -Action copy (Get-Content article.txt -Raw)
```

**方法3: クリップボードから渡す**
```powershell
# 記事をコピーしてから実行
Get-Clipboard | .\run-prompt.ps1 -PromptType note -Action copy
```

## 🔧 エイリアス設定（オプション）

より短いコマンドで実行したい場合、PowerShellプロファイルにエイリアスを追加できます。

### セットアップ

```powershell
# PowerShellプロファイルを開く
notepad $PROFILE

# 以下を追加
. "C:\Repos\note-articles\prompt\prompt-aliases.ps1"

# 保存して再起動
```

### エイリアス使用例

```powershell
# 記事プロンプトをコピー
prompt-note

# 商品プロンプトを表示
prompt-product -Action show

# 動画プロンプトをエディタで開く
prompt-video -Action open

# プロンプト一覧
prompt-list
```

## 📂 ファイル構成

```
prompt/
├── run-prompt.ps1              # メインスクリプト
├── prompt-aliases.ps1          # エイリアス定義（オプション）
├── PROMPT_RUNNER_GUIDE.md      # このファイル
├── note_prompt.txt             # 記事構成設計プロンプト
├── product_design_prompt.txt   # 商品設計プロンプト
└── ai_video_monetization_prompt.txt  # AI動画収益化プロンプト
```

## 🎓 ワークフロー例

### 完全な収益化フローを構築する場合

1. **商品設計**
   ```powershell
   .\run-prompt.ps1 -PromptType product -Action copy
   ```
   → ChatGPTでペルソナ分析→商品の核を作る

2. **動画で集客**
   ```powershell
   .\run-prompt.ps1 -PromptType video -Action copy
   ```
   → ChatGPTでSNS投稿文20本→自動化の仕組みを構築

3. **記事で教育**
   ```powershell
   .\run-prompt.ps1 -PromptType note -Action copy
   ```
   → ChatGPTで記事構成設計→ファン化

この3ステップで「**商品設計→動画集客→記事教育→自動販売**」が完成！

## ⚙️ カスタマイズ

### 特定セクションのみ表示/コピー

```powershell
# STEP 3のみ表示
.\run-prompt.ps1 -PromptType product -Action show -Section "STEP 3"

# タイトル設計部分のみコピー
.\run-prompt.ps1 -PromptType note -Action copy -Section "タイトル設計"
```

## 🐛 トラブルシューティング

### Q: 実行ポリシーエラーが出る

```powershell
# 実行ポリシーを確認
Get-ExecutionPolicy

# RemoteSigned に変更（管理者権限で実行）
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Q: VS Codeで開かない

```powershell
# VS Codeのパスを確認
Get-Command code

# パスが通っていない場合、手動で追加
$env:Path += ";C:\Users\YourName\AppData\Local\Programs\Microsoft VS Code\bin"
```

### Q: 文字化けする

```powershell
# UTF-8でエンコーディングを指定
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

## 📞 サポート

問題が発生した場合:
1. `.\run-prompt.ps1 -PromptType all` で一覧を確認
2. ファイルパスが正しいか確認
3. PowerShellのバージョンを確認（5.1以上推奨）

## 🎉 次のステップ

1. 各プロンプトを実際に試してみる
2. ChatGPTでの出力を確認
3. 自分のビジネスに合わせてカスタマイズ

**さあ、最強のプロンプトを使いこなそう！**
