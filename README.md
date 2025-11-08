# note 記事アーカイブ

このリポジトリは、note で公開する記事のソース管理・テンプレート保管・執筆支援ツールを統合したコンテンツ制作基地です。

## 📁 ディレクトリ構成

```
note-articles/
├── articles/           # 公開済み・執筆中の記事
│   ├── 2025-11-01_line-stamp-ai/
│   │   ├── article.md         # 記事本文
│   │   ├── prompts.txt        # 使用したプロンプト
│   │   ├── images/            # 記事用画像
│   │   └── metadata.json      # 公開日・タグ・URL等
│   └── ...
├── designs/            # 運用戦略・フレームワーク設計書
│   ├── x_api_operation_framework.md           # X API v2 総合フレームワーク
│   ├── ai_narrative_studio_operation_manual.md # AI Narrative Studio運用マニュアル
│   └── gethnote_operation_manual.md           # GETHNOTE運用マニュアル
├── templates/          # 記事テンプレート・プロンプトひな形
├── tools/              # 執筆支援・公開支援ツール
│   ├── x_api_analyzer.py      # X API v2分析ツール
│   └── x_api_setup_guide.md   # X API環境構築ガイド
└── drafts/             # 下書き・アイデアメモ
```

## 🎯 使い方

### 新しい記事を始める

```bash
# 今日の日付でディレクトリ作成
mkdir articles/$(date +%Y-%m-%d)_テーマ名

# テンプレートをコピー
cp templates/article_template.md articles/$(date +%Y-%m-%d)_テーマ名/article.md
```

### 記事を公開する

1. `article.md`を完成させる
2. `metadata.json`に公開情報を記入
3. note にコピペして公開
4. `metadata.json`に公開 URL を追記
5. コミット＆プッシュ

## 📝 記事一覧

| 日付       | タイトル                                             | ステータス | note URL       |
| ---------- | ---------------------------------------------------- | ---------- | -------------- |
| 2025-11-01 | 週末 D'AI'Y：AI でつくる！ユイの LINE スタンプ奮闘記 | ✅ 完成    | （公開後追記） |

## 🛠️ ツール

### 記事制作支援
- `tools/publish_to_note.py` - note API への自動投稿（将来実装予定）
- `tools/image_optimizer.py` - 画像サイズ最適化
- `tools/metadata_generator.py` - メタデータ自動生成

### X（旧Twitter）運用分析
- `tools/x_api_analyzer.py` - X API v2を使った投稿分析・レポート自動生成
- `tools/x_api_setup_guide.md` - 環境構築・トラブルシューティングガイド

## 📖 テンプレート

- `templates/article_template.md` - 基本記事構成
- `templates/prompt_template.txt` - AI プロンプト記録用
- `templates/metadata_template.json` - メタデータひな形

## 🎨 執筆ガイドライン

### タイトルの型

```
[損失] + [具体的数字] + [解決策] + [社会的証明] + [希少性]
```

例：「知らないと損！イラスト描けない私が週末 2 日で LINE スタンプ 16 種を完成させた AI 活用術【2025 年最新】」

### 構成の基本

1. **導入**（約 250 文字）：シーン描写で共感を生む
2. **本論 1**：問題の可視化
3. **本論 2**：具体的な解決策
4. **本論 3**：成果と実例
5. **結論**：変化のビジョン＋行動喚起

### 心理導線

```
共感 → 理解 → 希望 → 安心 → 行動
```

## 🔗 関連リンク

- [note 公式](https://note.com)
- [note ヘルプセンター](https://help.note.com)
- [Markdown 記法](https://help.note.com/hc/ja/articles/360000114182)

## 📋 運用戦略ドキュメント

### X（旧Twitter）運用フレームワーク

- **[X API v2 運用分析・最適化フレームワーク](designs/x_api_operation_framework.md)**  
  両アカウント共通の分析軸・データ取得設計・実装ロードマップ

- **[AI Narrative Studio 運用マニュアル](designs/ai_narrative_studio_operation_manual.md)**  
  30代会社員向け・信頼構築型の投稿戦術（月30投稿カレンダー・文体ルール・KPI追跡）

- **[GETHNOTE 運用マニュアル](designs/gethnote_operation_manual.md)**  
  底辺脱出層向け・損失回避刺激型の投稿戦術（月40投稿カレンダー・炎上管理・コミュニティ化）

### 実装ステップ
1. [X API環境構築ガイド](tools/x_api_setup_guide.md)を参照してAPI認証情報を取得
2. `tools/x_api_analyzer.py`で過去30日分のデータを取得・分析
3. 各運用マニュアルの投稿テンプレートを使って週次・月次で改善サイクルを回す

## 📊 パフォーマンス追跡

各記事の`metadata.json`に以下を記録：

- 公開日時
- 閲覧数（定期更新）
- スキ数
- コメント数
- 有料部分の販売数

## 🌟 今後の展開

### note記事制作
- [ ] note API 連携で自動投稿
- [ ] 画像生成 AI との統合ワークフロー
- [ ] 記事パフォーマンス分析ダッシュボード
- [ ] タグ別・カテゴリ別アーカイブ

### X運用最適化
- [ ] Phase 1（0-3ヶ月）：基盤構築・初期分析・競合調査
- [ ] Phase 2（4-6ヶ月）：感情分析導入・予測モデル構築
- [ ] Phase 3（7-12ヶ月）：自動化強化・収益化連携・ダッシュボード化

---

**Last Updated**: 2025-11-08
**Total Articles**: 1
**Status**: 🚀 稼働中
