# 📁 ディレクトリ管理ガイド

このドキュメントは、note-articlesプロジェクトのファイル整理ルールを説明します。

## 🎯 基本方針

**「作業種類ごとにフォルダを分ける」**
- 分析 → `analyses/`
- 設計 → `designs/`
- 記事 → `drafts/` → `articles/`

これにより、作業の蓄積が可視化され、過去の資産を活用できます。

---

## 📂 フォルダ構成

```
note-articles/
├── analyses/           # 📊 分析レポート
├── designs/            # 🎨 設計ドキュメント
├── drafts/             # 📝 下書き記事
├── articles/           # ✅ 投稿済み記事
├── templates/          # 📋 テンプレート
└── prompt/             # 💬 プロンプト集
```

---

## 📊 analyses/ - 分析レポート

### 保存される内容
- **心理診断:** 読者心理の4軸分析
- **ペルソナ分析:** 詳細なペルソナ設定
- **市場調査:** 競合分析、トレンド調査
- **構成設計:** 記事構成のアウトライン

### ファイル命名規則
```
YYYYMMDD_HHMMSS_分析種類_対象.md
```

### 例
```
20251103_143542_心理診断_AI動画で月10万稼ぐ方法.md
20251103_150000_ペルソナ分析_副業.md
20251103_153000_市場調査_AI動画市場.md
```

### いつ使う？
- `note_prompt.txt` で記事をリライトする際、**自動的に分析結果が保存**されます
- 商品設計・動画収益化で詳細なペルソナ分析が必要な場合

---

## 🎨 designs/ - 設計ドキュメント

### 保存される内容
- **商品設計:** ペルソナ100個→悩みTOP3→商品案10個
- **動画収益化プラン:** 収益化方法5つ、自動化フロー
- **SNS投稿文:** 20本セットの投稿文案
- **マネタイズ戦略:** ビジネスモデル設計

### ファイル命名規則
```
YYYYMMDD_HHMMSS_設計種類_対象.md
```

### 例
```
20251103_143542_商品設計_副業.md
20251103_150000_動画収益化プラン_AI生成動画.md
20251103_153000_SNS投稿文_YouTube戦略.md
```

### いつ使う？
- `product_design_prompt.txt` で商品設計を実行
- `ai_video_monetization_prompt.txt` で収益化プラン作成

---

## 📝 drafts/ - 下書き記事

### 保存される内容
- **リライト後の記事:** note投稿用Markdown
- **新規作成記事:** note用に最適化された記事
- **絵文字リッチ:** 30-50個の絵文字を含む

### ファイル命名規則
```
YYYYMMDD_HHMMSS_タイトル.md
```

### 例
```
20251103_143542_AI動画で月10万稼ぐ方法.md
20251103_150000_ChatGPT副業完全ガイド.md
```

### ファイル形式（Markdown）
```markdown
---
title: AI動画で月10万稼ぐ方法
created: 2025-11-03 14:35:42
source: note_prompt.txt
tags: AI, 副業, 動画編集
---

# 🎯 AI動画で月10万稼ぐ方法

（本文 - 絵文字30-50個）

---

## 📋 メタ情報
- 作成日時: 2025年11月03日 14:35
- 生成元: note_prompt.txt
- 文字数: 3,245文字
- 推定読了時間: 8分

## 🎯 次のアクション
- [ ] タイトル確認
- [ ] 誤字脱字チェック
- [ ] 絵文字最適化（30-50個）
- [ ] アイキャッチ画像準備
- [ ] noteに投稿
```

### いつ使う？
- `note_prompt.txt` で記事をリライト
- 商品設計・動画収益化の結果を記事化

---

## ✅ articles/ - 投稿済み記事

### 保存される内容
- **noteに投稿完了した記事**
- 投稿URLや投稿日時も含める

### ディレクトリ構造
```
articles/
├── 2025-11-01_line-stamp-ai/
│   ├── article.md
│   ├── images/
│   └── metadata.json
└── 2025-11-03_ai-video-monetization/
    ├── article.md
    └── metadata.json
```

### metadata.json の例
```json
{
  "title": "AI動画で月10万稼ぐ方法",
  "published_date": "2025-11-03",
  "note_url": "https://note.com/your-account/n/xxxx",
  "views": 1234,
  "likes": 56,
  "tags": ["AI", "副業", "動画編集"]
}
```

### いつ使う？
- noteに投稿後、**drafts/ から手動で移動**
- アーカイブとして保管

---

## 🔄 ファイルのライフサイクル

### 1. 記事リライトの場合

```
【入力】既存記事

↓ note_prompt.txt で処理

【出力1】analyses/YYYYMMDD_心理診断_タイトル.md
  - 心理診断
  - ペルソナ設定
  - 教育コンテンツ設計

【出力2】drafts/YYYYMMDD_タイトル.md
  - note投稿用Markdown
  - 絵文字30-50個

↓ noteに投稿

【移動】articles/YYYY-MM-DD_タイトル/
  - 投稿完了後、手動で移動
```

### 2. 商品設計の場合

```
【入力】業界名（例: 副業）

↓ product_design_prompt.txt で処理

【出力】designs/YYYYMMDD_商品設計_副業.md
  - ペルソナ100個
  - 悩みTOP3
  - 商品案10個

（オプション）note_prompt.txt で記事化

↓ drafts/YYYYMMDD_タイトル.md
```

### 3. 動画収益化の場合

```
【入力】なし（プロンプトのみ）

↓ ai_video_monetization_prompt.txt で処理

【出力】designs/YYYYMMDD_動画収益化プラン.md
  - 収益化方法5つ
  - SNS投稿文20本
  - 自動化フロー

（オプション）note_prompt.txt で記事化

↓ drafts/YYYYMMDD_タイトル.md
```

---

## 📌 ベストプラクティス

### ✅ DO（推奨）

1. **必ずタイムスタンプ付きファイル名**
   - `20251103_143542_タイトル.md`
   - 時系列で管理しやすい

2. **分析と記事を分離**
   - 分析: `analyses/`
   - 記事: `drafts/`
   - 投稿済み: `articles/`

3. **投稿後は必ず articles/ に移動**
   - drafts/ は常に「これから投稿するもの」だけ

4. **metadata.json を活用**
   - 投稿URL、閲覧数、いいね数を記録
   - 効果測定に使える

### ❌ DON'T（非推奨）

1. **ファイル名をマニュアルで変更しない**
   - タイムスタンプがずれると管理が混乱

2. **drafts/ に投稿済み記事を残さない**
   - articles/ に移動して整理

3. **分析結果を捨てない**
   - analyses/ に残しておけば、後で活用できる

---

## 🚀 実際の使用例

### 例1: 記事をリライトして投稿

```bash
# ステップ1: Copilot Chatでリライト
@workspace note_prompt.txtでこの記事をリライト（絵文字多め）→ 分析はanalyses、記事はdraftsに保存: （記事本文）

# 結果:
# - analyses/20251103_143542_心理診断_タイトル.md
# - drafts/20251103_143542_タイトル.md

# ステップ2: drafts/ のファイルを確認・編集

# ステップ3: noteに投稿
# https://note.com/new

# ステップ4: 投稿後、articles/ に移動
# drafts/20251103_143542_タイトル.md
# → articles/2025-11-03_タイトル/article.md
```

### 例2: 商品設計 → 記事化 → 投稿

```bash
# ステップ1: 商品設計
@workspace product_design_prompt.txtで「副業」の商品設計 → designs に保存

# 結果:
# - designs/20251103_143542_商品設計_副業.md

# ステップ2: 設計結果を記事化
@workspace note_prompt.txtで designs/20251103_143542_商品設計_副業.md を記事形式にリライト → drafts に保存

# 結果:
# - drafts/20251103_150000_副業で月10万稼ぐ商品設計.md

# ステップ3: noteに投稿 → articles/ に移動
```

---

## 📊 効果測定

### 各フォルダのファイル数をチェック

```powershell
# analyses/ の分析件数
(Get-ChildItem -Path "c:\Repos\note-articles\analyses" -Filter "*.md").Count

# designs/ の設計件数
(Get-ChildItem -Path "c:\Repos\note-articles\designs" -Filter "*.md").Count

# drafts/ の下書き件数
(Get-ChildItem -Path "c:\Repos\note-articles\drafts" -Filter "*.md").Count

# articles/ の投稿済み件数
(Get-ChildItem -Path "c:\Repos\note-articles\articles" -Directory).Count
```

### 月次レポート

```markdown
## 2025年11月の活動

- 📊 分析件数: 15件
- 🎨 設計件数: 8件
- 📝 記事作成: 12件
- ✅ note投稿: 10件
- 📈 平均閲覧数: 234回
- 💰 収益: ¥12,345
```

---

**これで、作業がちゃんと蓄積されていきます！🎉**
