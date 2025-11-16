# 📚 Prompt Knowledge Hub

プロンプトの蓄積・検索・運用・通知を一元管理するためのハブです。GitHub Copilot、Notion、LINEのどこからでも参照できるように、以下の4階層で整理しました。

1. **Inventory**: すべてのプロンプト一覧（カテゴリ、タイトル、概要、保管場所）
2. **Ops Manual**: 蓄積フロー／呼び出し方法の共通ルール
3. **Auto Maintenance**: 定期自動メンテのタスク設計
4. **Daily LINE Digest**: LINE通知での定時共有フロー

---

## 1. Inventory（カテゴリ別一覧）

| ID | カテゴリ | タイトル | 説明 | 保管ファイル | Copilot呼び出し例 |
|----|----------|----------|------|---------------|-------------------|
| M001 | Level1/マーケ | SNSバズ構成メモ | 3行構成で即投稿下書き | `prompt/COPILOT_PROMPT_LIBRARY_LEVELS.md` | `@workspace ... の M001 を実行` |
| M002 | Level2/マーケ | ニーズ→コンテンツマップ | ペルソナ＋教育設計3セット | 同上 | `@workspace ... の M002 を使って設計` |
| W001 | Level1/ライティング | 超速アウトライン化 | 5段構成アウトライン化 | 同上 | `W001` |
| W002 | Level2/ライティング | note記事ドラフト | 共感→課題→解決→成果→CTA | 同上 | `W002` |
| P001 | Level2/プロンプト | テンプレ管理ノート | タグ・入出力を整理 | 同上 | `P001` |
| P002 | Level3/プロンプト | Copilot指示テンプレ生成 | 要件→@workspace命令 | 同上 | `P002` |
| P003 | Level3/プロンプト | Python自動化スキャフォールド | Notion+OpenAI CLI雛形 | 同上 | `P003` |
| A001 | Level1/オートメモ | メモ整理バッチャー | 箇条書きをカテゴリ分類 | 同上 | `A001` |
| A002 | Level2/オペレーション | ファイル整理オートマタ | 出力→保存先提案 | 同上 | `A002` |
| A003 | Level3/自動化 | 連続リライト→保存 | `_queue` → `_done` 自動処理 | 同上 | `A003` |
| A004 | Level3/分析 | プロンプト評価レポート | 生成ログ採点 | 同上 | `A004` |
| NRW | noteリライト | note記事リライト完全版 | `note_prompt.txt`を参照して下書き保存 | `prompt/COPILOT_CHAT_PROMPTS.md` | `@workspace note_prompt...` |
| PRD | 商品設計 | 商品設計テンプレ | ペルソナ→商品案生成 | `prompt/product_design_prompt.txt` | `@workspace product_design_prompt...` |
| AVM | 動画収益化 | AI動画収益化プロンプト | 収益化案＋投稿文 | `prompt/ai_video_monetization_prompt.txt` | `@workspace ai_video_monetization_prompt...` |
| EDU | 教育カテゴリ投稿 | 6カテゴリ投稿生成 | `education_prompt_manager.py`用 | `tools/education_prompt_manager.py` | `python tools/education_prompt_manager.py` |

> **TIP:** 追加したいプロンプトは、この表にID/カテゴリ/概要を追記し、対応する `.txt` or `.md` ファイルを `prompt/` に配置してください。

---

## 2. Ops Manual（蓄積＆呼び出しフロー）

### 2.1 蓄積フロー（週次）
1. **インプット収集**: X、note、音声メモ → `Google Keep` → 毎週日曜にNotionへ移送
2. **Notion整備**: `Notion DB「Prompt Library」` に以下を登録
   - `ID`（連番＋カテゴリPrefix）
   - `Title`
   - `Category`（Marketing / Writing / Programming / Automation / Other）
   - `Source`（URLまたは日付）
   - `Usage Notes`
3. **Git同期**: 重要プロンプトは `.txt` or `.md` に書き起こし `prompt/` へコミット
4. **Hub更新**: 本`PROMPT_KNOWLEDGE_HUB.md`の表に行を追加

### 2.2 呼び出しルール
- VS Code: `Ctrl+Shift+I` → Chat → `@workspace prompt/COPILOT_PROMPT_LIBRARY_LEVELS.md の {ID}`
- CLI: `python tools/prompt_assistant.py --use {keyword}`（Level3導入後）
- Notion: DBで`Category` + `Tag`検索→ Copilotへ貼り付け

### 2.3 カテゴリ命名規則
```
M***: Marketing / 商品設計
W***: Writing / note構成
P***: Programming / プロンプト整備
A***: Automation / 自動処理
NRW, PRD, AVMなどは既存資産に合わせた専用ID
```

---

## 3. Auto Maintenance（自動メンテ計画）

| 頻度 | タスク | 実装案 |
|------|--------|--------|
| 毎日 00:00 | **Snapshot Export** | `python tools/prompt_snapshot.py --output data/prompt_snapshots/$(date).json`（新規作成予定）でNotion DB→JSON出力 |
| 毎週 日曜 | **Duplication Check** | Snapshot差分を比較し、タイトル重複/未使用（30日以上）を検出 → `analyses/prompt_audit_YYYYMMDD.md`を自動生成 |
| 毎月1日 | **Rotation Reminder** | 未更新ID一覧＋「更新推奨」コメントをLINE通知 |
| 随時 | **Expired Cleanup** | `status=archive` の行を `archive/` フォルダへ移動、Hub表から移譲 |

### 3.1 追加予定スクリプト
- `tools/prompt_snapshot.py`: Notion API→JSON/CSV保存、Gitコミット支援
- `tools/prompt_audit.py`: Snapshot差分→レポート生成
- `tools/prompt_digest.py`: 直近N件をまとめてLINE通知用テキスト生成

### 3.2 実行ガイド

**Snapshot Export**

```powershell
# NOTION_API_KEY / NOTION_DATABASE_ID を環境変数で設定しておく
python tools/prompt_snapshot.py --format both --pretty \
   --output-dir data/prompt_snapshots
```

- `--input-file <path>` を指定すると、既存JSONを読み込んでCSVだけ再生成可能
- JSONには `category_summary` が含まれるため、後続ジョブでカテゴリ別集計を再利用

**Digest Text**

```powershell
python tools/prompt_digest.py --mode daily \
   --snapshot-dir data/prompt_snapshots \
   --limit 5 --stale-days 30
```

- `--current`/`--previous` で比較対象を固定可能
- `--output digest/daily.txt` でLINE送信用の一時ファイルを生成
- `--json-output digest/daily.json` を渡すと n8n などで機械的に扱える統計が出力される

---

## 4. Daily LINE Digest（通知フロー）

### 4.1 ゴール
- 毎日 09:00 に「現行プロンプト一覧＋アップデート差分」をLINE Botで受信
- 週次でトレンド（追加/削除/未使用）もまとめる

### 4.2 既存資産との連携
- `tools/line_bot_api.py`（Flask, ポート5679）を利用
- `line_bot_state_manager.py` で「最終通知時刻」「未読差分」を保存
- n8n もしくは Windows Task Scheduler → `python tools/prompt_digest.py --mode daily` を実行

### 4.3 通知フォーマット例
```
[Prompt Digest / 2025-11-17 09:00]

■ 新規 (2)
- M005: TikTok 30秒台本
- A005: Copilot短縮コマンド生成

■ 更新 (1)
- W002: CTAテンプレを2025版に差し替え

■ 利用推奨 (3)
- 未使用30日: P001, A002, AVM

→ 詳細: PROMPT_KNOWLEDGE_HUB / Notionリンク
```

### 4.4 定時ジョブ例
```powershell
# Windows Task Scheduler 例 (毎日 09:00)
powershell.exe -NoProfile -Command "python C:\Repos\note-articles\tools\prompt_snapshot.py --format json --silent"
powershell.exe -NoProfile -Command "python C:\Repos\note-articles\tools\prompt_digest.py --mode daily | curl -X POST http://localhost:5679/notify --data-binary @-"
```
これらのコマンドは `run-prompt.ps1` や n8n から呼び出しても構いません。

---

## 5. 今後のアクション

1. **Notion DB** を最新情報で整備（ID付与・タグ統一・クラウドバックアップ）
2. `prompt_snapshot.py / prompt_digest.py` を実装し、Task Scheduler または n8n で自動化
3. LINE通知テンプレを `tools/prompt_manager/README.md` に追記
4. 月末に再びこのHubを更新し、陳腐化を防止

> このファイル自体を Copilot Chat で `@workspace prompt/PROMPT_KNOWLEDGE_HUB.md を要約して` と呼び出せば、最新状態をいつでも確認できます。
