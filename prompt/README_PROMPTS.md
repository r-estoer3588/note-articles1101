# 記事品質管理プロンプト - ファイル一覧

## 📂 プロンプトファイルの整理

### 🔵 記事生成用（既存）
- **`gethnote/prompt/geth_prompt.txt`** (1139行)
  - 用途: 新規記事の自動生成
  - 内容: ペルソナ設定、記事構成、データ検証ルール
  - 使用シーン: 0から記事を作る時

---

### 🟢 記事評価・改善用（新規作成）

#### 1. **`gesuinu_article_review_prompts.txt`** ⭐ コピペ用
- **用途**: げすいぬ版の記事レビュー・改善（実行用プロンプト集）
- **内容**: 8種類のコピペ用プロンプト
  - 基本プロンプト（単一記事）
  - 詳細版プロンプト（パターン指定）
  - チェックリスト版
  - NG→OK変換テーブル
  - 複数記事一括評価
  - Before/After比較
  - Pythonスクリプト生成
  - カスタマイズ例
- **使用シーン**: 記事をげすいぬ版で評価・改善したい時

---

#### 2. **`article_quality_evaluation_prompt_v3_gesuinu.txt`** 📖 詳細マニュアル（構造設計士版）
- **用途**: げすいぬ構造設計士ペルソナの評価基準・改善パターン集（完全版）
- **内容**:
  - 4指標の5段階定量評価基準
  - 改善パターン12種（Before/After例付き）
  - 正規表現パターン（Python）
  - 評価テンプレート + 構造設計士シグネチャチェック（表/フレーズ/フロー）
- **使用シーン**: 評価基準やペルソナ要件を詳細確認したい時

---

#### 3. **`article_quality_evaluation_prompt_v2.txt`** (846行)
- **用途**: 無難版の評価基準（げすいぬらしさ排除）
- **内容**:
  - 4指標の5段階定量評価基準
  - 改善パターン（「俺」→「私」、「カモ」→「損失」）
  - 実績データ（14記事改善結果）
- **使用シーン**: 炎上リスクを避けたい時

---

#### 4. **`article_quality_prompt_simple.txt`** (50行)
- **用途**: 簡易チェックリスト
- **内容**: ○/△/×での簡易判定
- **使用シーン**: 日常的な品質チェック

---

#### 5. **`article_quality_prompt_templates.txt`**
- **用途**: 10種類のコピペ用プロンプト（v2版）
- **内容**: 単一記事、複数記事、特定指標など
- **使用シーン**: v2（無難版）で評価したい時

---

#### 6. **`article_quality_evaluation_prompt.txt`** (旧版・非推奨)
- **用途**: 初期作成版（評価基準が抽象的）
- **内容**: 4指標の基本説明のみ
- **使用シーン**: 使わない（v2かv3を使う）

---

## 🎯 使い分けガイド

### 新規記事を作りたい
→ **`gethnote/prompt/geth_prompt.txt`**

### 既存記事をげすいぬ版で改善したい
→ **`gesuinu_article_review_prompts.txt`**（コピペ用）  
→ 詳細確認は **`article_quality_evaluation_prompt_v3_gesuinu.txt`**

### 既存記事を無難に改善したい
→ **`article_quality_prompt_templates.txt`**（コピペ用）  
→ 詳細確認は **`article_quality_evaluation_prompt_v2.txt`**

### 日常的な品質チェック
→ **`article_quality_prompt_simple.txt`**

---

## 📊 ファイル容量比較

| ファイル名 | 行数 | 用途 | 推奨度 |
|-----------|------|------|--------|
| geth_prompt.txt | 1139行 | 記事生成 | ⭐⭐⭐⭐⭐ |
| gesuinu_article_review_prompts.txt | 330行 | げすいぬ版レビュー | ⭐⭐⭐⭐⭐ |
| article_quality_evaluation_prompt_v3_gesuinu.txt | 680行 | げすいぬ構造設計士詳細 | ⭐⭐⭐⭐ |
| article_quality_evaluation_prompt_v2.txt | 846行 | 無難版詳細 | ⭐⭐⭐ |
| article_quality_prompt_templates.txt | 200行 | 無難版コピペ | ⭐⭐⭐ |
| article_quality_prompt_simple.txt | 50行 | 簡易チェック | ⭐⭐⭐⭐ |
| article_quality_evaluation_prompt.txt | 400行 | 旧版 | ❌ 非推奨 |

---

## 🚀 推奨ワークフロー

### 1. 新規記事作成
```
geth_prompt.txt でプロンプト実行
→ 記事生成
→ article_quality_prompt_simple.txt で簡易チェック
→ 問題あれば gesuinu_article_review_prompts.txt で改善
```

### 2. 既存記事の改善
```
gesuinu_article_review_prompts.txt から適切なプロンプトをコピペ
→ 記事を貼り付け
→ 自動改善
```

### 3. 大量の記事を一括改善
```
gesuinu_article_review_prompts.txt の「Pythonスクリプト生成プロンプト」
→ スクリプト生成
→ 一括実行
```

---

**更新日**: 2025年11月17日  
**管理者**: げすいぬ品質管理チーム
