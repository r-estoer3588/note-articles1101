# 📚 Note Articles Prompt Collection

GitHub Copilot Chatで直接使える、最強のnote記事作成プロンプト集

## 🚀 超簡単な使い方

### 1. GitHub Copilot Chatを開く

VS Codeで `Ctrl+Shift+I` （またはチャットアイコンをクリック）

### 2. プロンプトを貼り付け

以下のいずれかをコピペするだけ!

---

## 📝 記事リライトプロンプト

```
@workspace 以下のタスクを実行:
1. note_prompt.txt を読んで理解
2. 以下の記事をリライト
3. drafts/YYYYMMDD_HHMMSS_タイトル.md に保存（note投稿用Markdown形式）

【記事本文】
AIで書いたnote、なんか、つまらない。
読んでも心動かない。なぜなのか。

実は、AI×noteで難しいことがあるんよ。
ただAI使ってるだけだと「教育」ができない。

（以下、リライトしたい記事本文を貼り付け）
```

**ワンライナー版:**
```
@workspace note_prompt.txtでこの記事をリライトして drafts に保存: （記事本文）
```

**ファイル参照版:**
```
@workspace note_prompt.txt で drafts/input.txt をリライトして drafts に保存
```

---

## 🎯 商品設計プロンプト

```
@workspace 以下のタスクを実行:
1. product_design_prompt.txt を読んで理解
2. 「副業」業界のペルソナ100個→上位3つの悩み→商品案10個を生成
3. drafts/YYYYMMDD_商品設計_副業.md に保存
```

**ワンライナー版:**
```
@workspace product_design_prompt.txtで「副業」の商品設計して drafts に保存
```

**他の業界例:**
- `「婚活」の商品設計`
- `「英語学習」の商品設計`
- `「子育て」の商品設計`

---

## 🎬 AI動画収益化プロンプト

```
@workspace 以下のタスクを実行:
1. ai_video_monetization_prompt.txt を読んで理解
2. 収益化方法5つ→SNS投稿文20本→自動化の仕組みを生成
3. drafts/YYYYMMDD_動画収益化プラン.md に保存
```

**ワンライナー版:**
```
@workspace ai_video_monetization_prompt.txtで動画収益化プラン生成して drafts に保存
```

---

## 💡 実際の使用例

### 例1: 記事をリライトして即投稿

**あなた:**
```
@workspace note_prompt.txtでこの記事をリライト（絵文字多め）→ 分析はanalyses、記事はdraftsに保存:

AIで書いたnote、なんか、つまらない。
読んでも心動かない。なぜなのか。
（以下本文）
```

**Copilot:**
```
✅ リライト完了しました!

� 分析ファイル: analyses/20251103_143542_心理診断_AI動画で月10万稼ぐ方法.md
  - 読者心理の4軸診断
  - ペルソナ設定
  - 教育コンテンツ設計

📝 記事ファイル: drafts/20251103_143542_AI動画で月10万稼ぐ方法.md
  - 文字数: 3,245文字
  - 絵文字: 42個（note最適化済み）
  - 推定読了時間: 8分

次のステップ:
1. ファイルを確認・編集
2. noteに投稿（https://note.com/new）
3. 投稿後、articlesフォルダに移動
```

### 例2: 商品設計→記事作成→投稿の一気通貫

**ステップ1: 商品設計**
```
@workspace product_design_prompt.txtで「副業」の商品設計して drafts に保存
```

**ステップ2: 設計結果を記事化**
```
@workspace note_prompt.txtで drafts/20251103_商品設計_副業.md を記事形式にリライトして drafts に保存
```

**ステップ3: noteに投稿**
- draftsフォルダのMarkdownファイルをコピペ
- note.com で投稿

---

## 📂 ファイル構成

```
note-articles/
├── drafts/                          # 📝 リライト後の記事（note投稿用）
│   ├── 20251103_143542_タイトル.md
│   └── ...
├── analyses/                        # 📊 心理分析・市場分析
│   ├── 20251103_143542_心理診断_タイトル.md
│   ├── 20251103_150000_ペルソナ分析_副業.md
│   └── ...
├── designs/                         # 🎨 商品設計・収益化プラン
│   ├── 20251103_143542_商品設計_副業.md
│   ├── 20251103_150000_動画収益化プラン.md
│   └── ...
├── articles/                        # ✅ 投稿完了後、ここに移動
│   └── 2025-11-01_line-stamp-ai/
└── prompt/
    ├── note_prompt.txt                    # 記事リライト用
    ├── product_design_prompt.txt          # 商品設計用
    ├── ai_video_monetization_prompt.txt   # 動画収益化用
    └── README.md                          # このファイル
```

### 📂 各フォルダの役割

| フォルダ | 用途 | 保存されるファイル |
|---------|------|------------------|
| **drafts/** | note投稿用記事 | リライト後のMarkdown（絵文字リッチ） |
| **analyses/** | 分析レポート | 心理診断、ペルソナ分析、市場調査 |
| **designs/** | 設計ドキュメント | 商品設計、収益化プラン、SNS投稿文 |
| **articles/** | 投稿完了記事 | noteに投稿済みの記事（手動移動） |
| **prompt/** | プロンプト集 | 各種プロンプトファイル |

---

## 🎯 保存されるファイル形式

**ファイル名:** `20251103_143542_AI動画で月10万稼ぐ方法.md`

**内容:**
```markdown
---
title: AI動画で月10万稼ぐ方法
created: 2025-11-03 14:35:42
source: GitHub Copilot Chat
---

# AI動画で月10万稼ぐ方法

（リライト後の本文）

---

## メタ情報
- 作成日時: 2025年11月03日 14:35
- 生成元: note_prompt.txt
- ステータス: 下書き

## 次のアクション
- [ ] タイトルの最終確認
- [ ] 本文の誤字脱字チェック
- [ ] noteに投稿
- [ ] SNSでシェア
```

---

## 🔥 応用テクニック

### 連続リライト

```
@workspace note_prompt.txtで以下の3記事を一括リライトして drafts に保存:
1. drafts/draft1.txt
2. drafts/draft2.txt
3. drafts/draft3.txt
```

### カスタマイズ指定

```
@workspace note_prompt.txtでリライト。タイトルは「〇〇」、文字数は3000文字以内、トーンはカジュアルで drafts に保存:
（記事本文）
```

### 他プロンプトとの併用

```
@workspace 以下を順番に実行:
1. product_design_prompt.txtで「副業」の商品設計
2. その商品を note_prompt.txt で記事化
3. drafts に両方保存
```

---

## 💬 便利なショートカット

よく使うプロンプトを登録しておくと便利:

### VS Code User Snippets

1. `Ctrl+Shift+P` → "Configure User Snippets"
2. "markdown.json" を選択
3. 以下を追加:

```json
{
  "Note Rewrite": {
    "prefix": "note-rewrite",
    "body": [
      "@workspace note_prompt.txtでこの記事をリライトして drafts に保存:",
      "$1"
    ],
    "description": "note記事リライトプロンプト"
  },
  "Product Design": {
    "prefix": "product-design",
    "body": [
      "@workspace product_design_prompt.txtで「$1」の商品設計して drafts に保存"
    ],
    "description": "商品設計プロンプト"
  },
  "Video Monetization": {
    "prefix": "video-monetize",
    "body": [
      "@workspace ai_video_monetization_prompt.txtで動画収益化プラン生成して drafts に保存"
    ],
    "description": "動画収益化プロンプト"
  }
}
```

**使い方:**
- Copilot Chatで `note-rewrite` と入力 → Tab
- 自動的にプロンプトが展開される

---

## 🎉 メリット

✅ **コマンド不要** - Chatに貼り付けるだけ
✅ **ファイル自動保存** - draftsフォルダに自動保存
✅ **note即投稿可能** - Markdown形式で出力
✅ **履歴管理** - タイムスタンプ付きファイル名
✅ **VS Code統合** - エディタ内で完結

---

## 🔧 トラブルシューティング

### Q: ファイルが保存されない

**A:** draftsフォルダが存在するか確認
```
@workspace drafts フォルダを作成
```

### Q: プロンプトが長すぎる

**A:** ワンライナー版を使用
```
@workspace note_prompt.txtで（記事）をリライト
```

### Q: タイトルが正しく抽出されない

**A:** 手動指定
```
@workspace note_prompt.txtでリライト。タイトルは「〇〇」で保存:（記事）
```

---

## 📞 サポート

問題が発生した場合:
1. プロンプトファイル（.txt）が存在するか確認
2. draftsフォルダが存在するか確認
3. GitHub Copilotが有効になっているか確認

---

**さあ、GitHub Copilot Chatで爆速記事作成を始めよう!**
