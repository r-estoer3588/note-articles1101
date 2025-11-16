# 🤖 GitHub Copilot Prompt Library Hub

GitHub Copilot Chatだけでプロンプトを呼び出し・編集・実行できるように、カテゴリ別のライブラリをこのファイルに集約しました。VS Code上でチャットに以下のように入力するだけで、Copilotが該当セクションを読み込みます。

```
@workspace prompt/COPILOT_PROMPT_LIBRARY_LEVELS.md から M001 を参照して実行してください
```

---

## 🧭 使い方クイックガイド

| 操作 | Copilotチャット例 |
|------|-------------------|
| プロンプトを実行 | `@workspace prompt/COPILOT_PROMPT_LIBRARY_LEVELS.md の M001 を使って下書きを作成` |
| 複数指定 | `@workspace prompt/COPILOT_PROMPT_LIBRARY_LEVELS.md の M002 と W001 を順番に実行` |
| 新規追加 | `@workspace prompt/COPILOT_PROMPT_LIBRARY_LEVELS.md に P004 (LLM評価自動化) を追加して` |
| 要約だけ欲しい | `@workspace prompt/COPILOT_PROMPT_LIBRARY_LEVELS.md を要約して、使えそうなものを3つ紹介して` |

`M***` = Marketing, `W***` = Writing, `P***` = Programming, `A***` = Automation。

---

## 🟢 Level 1（メモ速記 / Google Keep相当）

スマホで拾ったネタをそのまま下書き化するための超軽量プロンプト。Copilotで素早く文章化したいときに使用。

### M001: SNSバズ構成メモ
```
あなたはSNSバズハンターです。
以下のネタメモを読み、30秒以内に投稿できる下書きを3本作成してください。

# 制約
- フック → 共感 → オチ の3行構成
- 絵文字は2個以内
- ハッシュタグ不要

# 入力
{{ネタメモ}}
```

### W001: 超速アウトライン化
```
メモを5段階構成のアウトラインに変換してください。
1. 共感
2. 課題の明確化
3. 体験/ストーリー
4. 解決策
5. CTA

各セクションは80文字以内。
入力: {{メモ}}
```

### A001: メモ整理バッチャー
```
複数の箇条書きメモを読み、カテゴリ別にまとめてください。
- マーケ: 🔵
- ライティング: 🟠
- プログラミング: 🟣
- その他: ⚪

出力は以下のJSON:
{
  "category": "🔵 マーケ",
  "idea": "...",
  "アクション": "..."
}
```

---

## 🟠 Level 2（情報整理 / Notion相当）

Notionデータベースと同じ粒度で整理・タグ付けしたいときのプロンプト群。

### M002: ニーズ→コンテンツマップ
```
あなたはnoteグロースコンサルタントです。
以下の読者インサイトを読み、
- ペルソナ
- 悩み
- 必要な教育
- 提示する未来
- CTA
を1セットとして3セット作成してください。
入力: {{読者インサイト}}
```

### W002: note記事ドラフト
```
noteテンプレ(共感→課題→解決→成果→CTA)に沿って、見出し+箇条書きで骨子を作成してください。
- 文字数: 各セクション200字以内
- 絵文字: 各セクション1つ
- CTAは「noteの売り場」を想定
入力: {{キーワードor概要}}
```

### P001: テンプレ管理ノート
```
以下のプロンプト案を読み、
1. タグ（最大3つ）
2. 想定ユースケース
3. 入出力サンプル
を整理してください。
入力: {{プロンプト案}} 
```

### A002: ファイル整理オートマタ
```
以下の生成結果を分類して、保存先フォルダと推奨ファイル名を提案してください。
フォルダ候補: drafts / analyses / designs / articles
命名規則: YYYYMMDD_HHMMSS_用途_タイトル
入力: {{出力冒頭100行}}
```

---

## 🔵 Level 3（自動化 / Notion+Python相当）

Copilotから直接指示して、定型ワークフローを全自動化するときのプロンプト群。

### A003: 連続リライト→保存
```
@workspace 以下の手順で処理してください:
1. prompt/note_prompt.txt を読む
2. drafts/ フォルダ内の `*_queue.md` をすべて探索
3. 各ファイルを note_prompt の基準でリライト
4. 元ファイルを `_queue.md` → `_done.md` にリネーム
5. 変更一覧を出力
```

### A004: プロンプト評価レポート
```
以下の生成ログを読み、
- プロンプトID
- 成功/失敗
- 修正案
- 推奨ID（M/W/P/A）
を表形式でまとめてください。
入力: {{ログ}}
```

### P002: GitHub Copilot指示テンプレ生成
```
以下の要件をGitHub Copilot Chat用の`@workspace`命令に変換してください。
必須項目: 対象ファイル/処理ステップ/保存先/報告内容
入力: {{要件}}
```

### P003: Python自動化スキャフォールド
```
Notion + OpenAI API連携スクリプトの雛形を生成してください。
- CLI引数でクエリ指定
- Notion query → OpenAI呼び出し → 結果を`outputs/YYYYMMDD_result.json`に保存
- ログ出力あり
```

---

## 🛠️ Copilotへの追加登録方法

```
@workspace prompt/COPILOT_PROMPT_LIBRARY_LEVELS.md に P004 を追加。
内容:
P004: LLM評価自動化
- 目的: 生成物を自動採点
- 入力: 生成テキスト
- 出力: 採点(0-100), Good/Badポイント, 修正案
```

Copilotはこの指示を受けると、本ファイルの適切な位置に追記します。

---

## 📌 運用ヒント

- **ファイルは1つに集約**: Copilotはファイル名を参照できるため、`COPILOT_PROMPT_LIBRARY_LEVELS.md`にまとめると迷子になりません。
- **IDで呼び出し**: `M001で`と指定するだけで該当セクションを探せます。
- **差分コミットが楽**: 変更はGit管理されるため、履歴追跡も簡単。

---

これで、面倒なワークフローを作り込まなくても、GitHub Copilotチャットだけでプロンプト資産を呼び出し・更新・実行できる状態になりました。気になるプロンプトがあれば、`@workspace prompt/COPILOT_PROMPT_LIBRARY_LEVELS.md を要約して`と聞けば、Copilotが使い所まで説明してくれます。