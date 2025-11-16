# note-articles ツール一覧

このディレクトリには、note記事制作とX運用を効率化するための各種ツールが格納されています。

## 📁 ディレクトリ構造

```
tools/
├── prompt_manager/          # 🆕 プロンプト自動管理システム
├── x_api_analyzer.py        # X API分析ツール
├── generate_articles.py     # AI記事生成支援
└── ...（その他ツール）
```

---

## 🆕 プロンプト自動管理システム

**完全無料・スマホ完結・プログラミング不要**のプロンプト管理システム。

### 機能
- LINEで送信→Notionに自動保存
- AI自動カテゴリ分類・タグ付け
- 高速検索・一覧表示
- PC/スマホ完全同期

### ドキュメント
- [README.md](prompt_manager/README.md) - システム詳細仕様
- [QUICKSTART.md](prompt_manager/QUICKSTART.md) - 15分セットアップガイド
- [note_article_template.md](prompt_manager/note_article_template.md) - note記事テンプレート
- [SCREENSHOT_GUIDE.md](prompt_manager/SCREENSHOT_GUIDE.md) - スクリーンショット撮影ガイド
- [TROUBLESHOOTING.md](prompt_manager/TROUBLESHOOTING.md) - トラブルシューティング

### クイックスタート
```powershell
cd prompt_manager
# QUICKSTART.mdの手順に従ってセットアップ（15分）
```

### スナップショット＆ダイジェスト自動化
- `prompt_snapshot.py` : NotionのPrompt LibraryをJSON/CSVにエクスポート
- `prompt_digest.py` : 2つのスナップショットを比較してLINE送信用文面を生成

```powershell
# 1) 日次でNotionをエクスポート
python prompt_snapshot.py --format both --pretty --output-dir ..\data\prompt_snapshots

# 2) 最新スナップショットの差分をLINEダイジェスト化
python prompt_digest.py --mode daily --limit 5 --stale-days 30 \
	--snapshot-dir ..\data\prompt_snapshots
```

`prompt_snapshot.py --input-file <existing.json> --format csv` のように既存スナップショットからCSVだけ再生成することもできます。

---

## X API分析ツール

### 概要
X API v2を使用した投稿分析・レポート自動生成ツール。

### 機能
- 投稿データ取得（インプレッション、エンゲージメント）
- 時系列分析・トレンド検出
- レポート自動生成（Markdown/CSV）

### 使い方
```powershell
python x_api_analyzer.py
```

### 詳細
[x_api_setup_guide.md](x_api_setup_guide.md) を参照。

---

## 📦 アーカイブ済み（LINE Bot関連）

LINE Bot メニュー/LINE連携ワークフロー一式は 2025-11-16 に撤去され、`archive/line_bot/` に移動しました。再開する場合はそちらの README を参照してください。

---

## AI記事生成支援

### 概要
note記事の自動生成・品質向上支援ツール群。

### ツール一覧

#### 基本生成
- `generate_articles.py` - 基本記事生成
- `premium_article_generator_v4.py` - プレミアム品質生成

#### 品質向上
- `article_polisher.py` - 記事磨き上げ
- `ultimate_quality_upgrade.py` - 最終品質アップグレード

#### バッチ処理
- `bulk_improve_articles_v3_gesuinu.py` - 一括改善（GETHNOTE用）

### 使い方
```powershell
# 記事生成
python generate_articles.py

# 品質向上
python article_polisher.py input/draft.md
```

---

## その他のツール

### 画像生成・最適化
- `generate_plush_image.py` - ぬいぐるみ画像生成
- `image_optimizer.py` - 画像最適化（圧縮・リサイズ）

### データ収集・分析
- `analyze_categories.py` - カテゴリ分析
- `verified_data_sources.py` - データソース検証

### note自動投稿
- `note_auto_poster.py` - note自動投稿ツール
- [NOTE_AUTO_POSTER_GUIDE.md](NOTE_AUTO_POSTER_GUIDE.md)

### ファイル管理
- `rename_article_files.py` - 記事ファイル名一括変更
- `deduplicate_articles.py` - 重複記事削除

---

## 🚀 よく使うコマンド

### 開発環境セットアップ
```powershell
# 仮想環境作成
python -m venv venv

# 仮想環境有効化
.\venv\Scripts\Activate.ps1

# 依存関係インストール
pip install -r ../requirements.txt
```

### X API分析実行
```powershell
python x_api_analyzer.py
```

---

## 📚 関連ドキュメント

### セットアップガイド
- [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md) - 全体クイックスタート

### ワークフローガイド
- [N8N_WORKFLOW_GUIDE.md](N8N_WORKFLOW_GUIDE.md) - n8nワークフロー設計
- [LEARN_WORKFLOW_GUIDE.md](LEARN_WORKFLOW_GUIDE.md) - 学習ワークフロー

### 実装サマリー
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - 実装詳細

---

## 🐛 トラブルシューティング

### 一般的な問題

#### ポート競合
```powershell
# ポート5679使用中の確認
netstat -ano | findstr :5679

# プロセス終了
taskkill /PID <PID> /F
```

#### 依存関係エラー
```powershell
# 再インストール
pip install --force-reinstall -r ../requirements.txt
```

#### 環境変数未設定
```powershell
# .envファイル確認
cat .env.template

# 環境変数設定例
$env:LINE_CHANNEL_SECRET="your_secret"
$env:LINE_CHANNEL_ACCESS_TOKEN="your_token"
```

---

## 📞 サポート

### 内部ドキュメント
各ツールの詳細は、対応するREADME/ガイドを参照。

### 外部リソース
- [Notion API Docs](https://developers.notion.com/)
- [LINE Developers](https://developers.line.biz/ja/)
- [n8n Documentation](https://docs.n8n.io/)
- [X API Documentation](https://developer.twitter.com/en/docs)

---

**最終更新**: 2025-11-16  
**管理者**: AI Narrative Studio
