# note記事アーカイブ

このリポジトリは、noteで公開する記事のソース管理・テンプレート保管・執筆支援ツールを統合したコンテンツ制作基地です。

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
├── templates/          # 記事テンプレート・プロンプトひな形
├── tools/              # 執筆支援・公開支援ツール
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
3. noteにコピペして公開
4. `metadata.json`に公開URLを追記
5. コミット＆プッシュ

## 📝 記事一覧

| 日付 | タイトル | ステータス | note URL |
|------|---------|-----------|----------|
| 2025-11-01 | 週末D'AI'Y：AIでつくる！ユイのLINEスタンプ奮闘記 | ✅ 完成 | （公開後追記） |

## 🛠️ ツール

- `tools/publish_to_note.py` - note APIへの自動投稿（将来実装予定）
- `tools/image_optimizer.py` - 画像サイズ最適化
- `tools/metadata_generator.py` - メタデータ自動生成

## 📖 テンプレート

- `templates/article_template.md` - 基本記事構成
- `templates/prompt_template.txt` - AIプロンプト記録用
- `templates/metadata_template.json` - メタデータひな形

## 🎨 執筆ガイドライン

### タイトルの型

```
[損失] + [具体的数字] + [解決策] + [社会的証明] + [希少性]
```

例：「知らないと損！イラスト描けない私が週末2日でLINEスタンプ16種を完成させたAI活用術【2025年最新】」

### 構成の基本

1. **導入**（約250文字）：シーン描写で共感を生む
2. **本論1**：問題の可視化
3. **本論2**：具体的な解決策
4. **本論3**：成果と実例
5. **結論**：変化のビジョン＋行動喚起

### 心理導線

```
共感 → 理解 → 希望 → 安心 → 行動
```

## 🔗 関連リンク

- [note公式](https://note.com)
- [noteヘルプセンター](https://help.note.com)
- [Markdown記法](https://help.note.com/hc/ja/articles/360000114182)

## 📊 パフォーマンス追跡

各記事の`metadata.json`に以下を記録：

- 公開日時
- 閲覧数（定期更新）
- スキ数
- コメント数
- 有料部分の販売数

## 🌟 今後の展開

- [ ] note API連携で自動投稿
- [ ] 画像生成AIとの統合ワークフロー
- [ ] 記事パフォーマンス分析ダッシュボード
- [ ] タグ別・カテゴリ別アーカイブ

---

**Last Updated**: 2025-11-01
**Total Articles**: 1
**Status**: 🚀 稼働中
