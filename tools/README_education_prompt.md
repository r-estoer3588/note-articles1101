# 教育カテゴリ別投稿生成ツール

## 🎯 できること

**ワンストップで投稿案を自動生成！**

1. カテゴリ選択（信用/目的/問題/手段/投資/行動）
2. 4項目を入力（ゴール/ペルソナ/問題点/トーン）
3. テーマ入力（何について書くか）
4. **→ AIが3つの投稿案を自動生成！**

## 🚀 使い方

### 基本（対話モード）
```powershell
python tools/education_prompt_manager.py
```

### コマンドライン（従来通り）
```powershell
# 一覧表示
python tools/education_prompt_manager.py --list

# テンプレ表示
python tools/education_prompt_manager.py --show 信用

# プリフィル
python tools/education_prompt_manager.py --prefill 行動 --goal "登録" --persona "30代" --pain "先延ばし" --tone "緊急性"
```

## 🔑 自動生成の設定（任意）

### 1. OpenAI APIキー取得
https://platform.openai.com/api-keys

### 2. ライブラリインストール
```powershell
pip install openai pyperclip
```

### 3. 環境変数設定
```powershell
# 一時的（現在のセッションのみ）
$env:OPENAI_API_KEY = "sk-proj-..."

# 永続的（推奨）
[System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "sk-proj-...", "User")
```

### 4. 確認
```powershell
python tools/education_prompt_manager.py
```
→ テーマ入力後、自動で投稿案が生成されます！

## 💡 API未設定でも使える

API未設定の場合は：
- システムプロンプトのみ表示
- ChatGPT/Claude等に貼り付けて使用
- クリップボードに自動コピー

## 📝 入力例

| 項目 | 入力例 |
|------|--------|
| カテゴリ | 1（信用の教育） |
| ゴール | note記事を読んでもらう |
| ペルソナ | 30代会社員/副業に挑戦中 |
| 問題点 | 時間がなくて継続できない |
| トーン | 共感的で落ち着いた |
| テーマ | 1日15分でできる副業習慣 |

## 🎨 カテゴリ説明

| 番号 | カテゴリ | 目的 |
|------|----------|------|
| 1 | 信用 | 信頼・共感・安心感の構築 |
| 2 | 目的 | 理想未来の明確化と動機形成 |
| 3 | 問題 | 現状の限界と真因認識 |
| 4 | 手段 | 解決策の期待醸成 |
| 5 | 投資 | コストの正当化と価値提示 |
| 6 | 行動 | 即時アクション誘発 |

## 🛠️ トラブルシューティング

### 「openaiライブラリが必要です」
```powershell
pip install openai
```

### 「API呼び出しエラー」
- APIキーが正しく設定されているか確認
- 残高があるか確認（https://platform.openai.com/usage）
- インターネット接続確認

### クリップボードコピーが動かない
```powershell
pip install pyperclip
```

## 📄 関連ファイル

- `education_prompt_manager.py` - メインスクリプト
- `../prompt/education_prompts.md` - 全テンプレート詳細
- `.env.example` - 環境変数設定サンプル
