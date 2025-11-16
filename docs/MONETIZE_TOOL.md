# 💰 SNSマネタイズプラン生成ツール

あなたの人生を変える、本気のSNSマネタイズプランを設計するツールです。

## 🎯 概要

10年以上のSNSマーケティング経験を持つ戦略コンサルタントの視点で、
あなた専用の超具体的なマネタイズプランを生成します。

### 特徴

- **STEP1: 現状の深掘り分析**
  - 5つのカテゴリ、計20以上の質問
  - 対話型で一つずつ丁寧に回答
  - 回答はJSON形式で保存・再利用可能

- **STEP2: 包括的プラン生成**
  - 1万文字以上の超具体的プラン
  - 90日実行プラン（週次タスク）
  - マネタイズ戦略（即金型/積み上げ型/資産型）
  - バズる投稿テンプレート
  - 収益目標とKPI
  - リスクヘッジ戦略

## 🚀 クイックスタート

### 1. セットアップ

```powershell
monetize -Setup
```

以下が自動でチェック・インストールされます：
- Python環境
- 依存パッケージ（openai, pyperclip）
- OpenAI API Key設定（オプション）
- 出力ディレクトリ作成

### 2. プラン生成

#### パターンA: 対話型（推奨）

```powershell
monetize
```

質問に一つずつ答えていき、最後にプロンプトを生成。
GitHub Copilot Chatに貼り付けて使用。

#### パターンB: OpenAI API自動生成

```powershell
monetize -Api
```

OPENAI_API_KEYが設定されていれば、自動でプラン生成。

#### パターンC: プロンプトのみ生成

```powershell
monetize -PromptOnly
```

プロンプトのみ生成してクリップボードにコピー。

## 📋 STEP1: 現状の深掘り分析

5つのカテゴリで状況を深く理解します：

### 1. 現在の状況
- 職業・年齢・居住地
- 月収と、理想の月収
- SNS運用歴
- 現在のフォロワー数

### 2. スキル・経験の棚卸し
- 仕事で培ったスキル
- 趣味や特技
- 「これなら3時間語れる」というテーマ
- 過去の成功経験
- 人から相談されること

### 3. リソース確認
- SNSに使える時間
- 初期投資可能額
- 協力者の有無
- 既存のコンテンツ資産

### 4. 目標とマインド
- 3ヶ月後の理想状態
- 1年後の収益目標
- やりたくないこと
- 譲れない価値観

### 5. 過去の失敗・課題
- SNSで挫折した経験
- 続かなかった理由
- 動けない障害

## 📊 STEP2: 戦略設計（出力内容）

### ✅ 生成されるプラン内容

1. **あなたの最強ポジション分析**
   - 市場価値が高いスキルTOP3
   - 競合が少ない独自の強み
   - マネタイズしやすい切り口
   - 「この人といえば◯◯」ポジション提案

2. **ターゲット顧客の明確化**
   - 最も刺さる顧客像（ペルソナ）
   - その人が抱える悩みTOP5
   - 課金余力
   - よく見るSNSプラットフォーム

3. **SNS戦略（プラットフォーム別）**
   - メインSNS（濃い発信）
   - サブSNS（導線）
   - マネタイズ先（最終収益化）

4. **マネタイズ戦略（3パターン）**
   - 即金型（30日以内に収益）
   - 積み上げ型（3〜6ヶ月で安定収益）
   - 資産型（6ヶ月〜1年で不労所得化）

5. **90日実行プラン**
   - 1ヶ月目: 土台作り（週次タスク）
   - 2ヶ月目: 加速
   - 3ヶ月目: 収益化本格化

6. **コンテンツ戦略**
   - バズる投稿テンプレート3選
   - ストック型コンテンツ10本

7. **収益目標とKPI**
   - 1ヶ月目/3ヶ月目/6ヶ月目の目標

8. **よくある失敗と回避策**

9. **リスクヘッジ戦略**

10. **あなた専用の成功の方程式**

## 📁 出力ファイル

```
outputs/monetize/
  ├─ step1_answers_20251116_120000.json  # STEP1回答データ
  ├─ prompt_20251116_120000.txt          # 生成されたプロンプト
  └─ monetize_plan_20251116_120000.md    # 最終プラン（-Api使用時）
```

## 🔧 コマンドリファレンス

### 基本コマンド

```powershell
# 対話型で質問に回答
monetize

# ヘルプ表示
monetize -Help

# セットアップ
monetize -Setup
```

### 高度な使い方

```powershell
# OpenAI APIで自動生成
monetize -Api

# プロンプトのみ生成
monetize -PromptOnly

# 保存済み回答を読み込んでプラン生成
monetize -Load outputs/monetize/step1_answers_20251116_120000.json -Api

# 短縮エイリアス
mz
mz -Help
mz -Api
```

## 🔑 OpenAI API設定

### 方法1: セットアップで対話的に設定

```powershell
monetize -Setup
# → "API Keyを設定しますか？" で y を選択
```

### 方法2: 環境変数に手動設定

```powershell
# 現在のセッションのみ
$env:OPENAI_API_KEY = "sk-..."

# PowerShellプロファイルに永続化
notepad $PROFILE
```

プロファイルに追加：

```powershell
# OpenAI API Key
$env:OPENAI_API_KEY = "sk-..."
```

### 方法3: GitHub Copilot Chat統合

API Keyなしでも使用可能！

1. `monetize -PromptOnly` で実行
2. 生成されたプロンプトがクリップボードにコピーされる
3. GitHub Copilot Chatに貼り付け
4. AIが本気のプランを生成

## 💡 使い方の例

### 例1: 初めて使う場合

```powershell
# 1. セットアップ
monetize -Setup

# 2. 対話型で質問に回答
monetize

# 3. 生成されたプロンプトをGitHub Copilot Chatに貼り付け
```

### 例2: OpenAI APIで完全自動

```powershell
# 1. API Key設定（初回のみ）
monetize -Setup

# 2. 質問に回答 & 自動生成
monetize -Api
```

### 例3: 回答を保存して後で生成

```powershell
# 1. 質問に回答（プロンプトのみ生成）
monetize -PromptOnly

# 2. 後日、保存済み回答から再生成
monetize -Load outputs/monetize/step1_answers_20251116_120000.json -Api
```

## 🎨 出力の品質

### プランの特徴

- ✅ 抽象論NG。全て具体的な数字と行動レベル
- ✅ 「〜すると良い」ではなく「〜する」と断言
- ✅ 再現性重視。誰がやっても結果が出る設計
- ✅ 「これなら自分でもできる」と思える難易度
- ✅ 1万文字以上の超具体的プラン
- ✅ 「この人、本気で私の人生変えようとしてくれてる」という熱量

### プランのカスタマイズ度

- テンプレートではなく、**あなたの状況に100%カスタマイズ**
- あなたの強み・経験・リソースを**最大限活かす**
- **最短距離で結果を出せる戦略**

## 🔍 トラブルシューティング

### Python not found

```powershell
monetize -Setup
# → Pythonインストールガイドが表示される
```

https://www.python.org/downloads/ からインストール

### パッケージがない

```powershell
monetize -Setup
# → 自動でインストールを提案
```

または手動で：

```powershell
pip install openai pyperclip
```

### OpenAI API呼び出しエラー

```powershell
# API Key確認
echo $env:OPENAI_API_KEY

# 再設定
monetize -Setup
```

### プロンプトが長すぎる

GitHub Copilot Chatの入力制限に引っかかる場合：

1. 生成された `prompt_*.txt` ファイルを開く
2. 分割して複数回に分けて入力
3. または `-Api` オプションで直接生成

## 📚 関連ファイル

- `C:\Repos\note-articles\monetize.ps1` - ランチャースクリプト
- `C:\Repos\note-articles\tools\monetize_planner.py` - メインツール
- `C:\Repos\note-articles\tools\profile_snippet_monetize.ps1` - プロファイル用スニペット
- `C:\Repos\note-articles\outputs\monetize\` - 出力ディレクトリ

## 🚀 次のステップ

1. **セットアップ**: `monetize -Setup`
2. **プラン生成**: `monetize`
3. **実行**: 生成された90日プランに従って行動開始！

---

**人生を変える覚悟で、本気のプランを作りましょう。**
