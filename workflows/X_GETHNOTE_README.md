# X 自動運用（GETHNOTE 専用）

GETHNOTE（有料 note 量産）に最適化した X（旧 Twitter）自動投稿の設計とセットアップ手順です。既存の Notes→Notion とは独立運用です。

---

## 目的と方針

- 目的: 30日×1日3本の販売記事を、X で安全かつ継続的に拡散して購買導線へ送客
- 連携元: `gethnote/schedule/tracking_sheet.csv`（配信カレンダー）
- 連携先: X（旧 Twitter）投稿。任意でスレッド化・画像添付にも対応
- 品質/コンプライアンス: X 規約と法規に抵触しないように、文面生成に安全フィルタと AI ガードレールを併用

---

## 全体アーキテクチャ

1) Cron（5分毎）
2) スケジュール CSV を読み込み（当該時刻±8分の行だけ抽出）
3) 行に `note_url` があれば優先採用、なければ投稿スキップ（導線未準備の防止）
4) OpenAI で「安全・簡潔・クリック導線重視」の X 文面を生成（最大 220 文字、3 ハッシュタグ）
5) セーフティフィルタ（侮蔑/差別/過激煽り/医療・金融断定表現の簡易除去）
6) 画像パスがあれば最適化（オプション）→ メディア添付
7) X に投稿（単発 or スレッド 2-3 本）
8) `posted.json` にユニークキー（`日付|配信時刻|記事ID`）を書き込み、二重投稿防止
9) 投稿結果を `tracking_sheet.csv` の該当行に反映（任意。まずは `posted.json` のみでも運用可）

---

## 必要ファイル（このリポジトリに追加済み）

- `workflows/x-gethnote-auto-poster.json` … n8n インポート用ワークフロー雛形
- `gethnote/schedule/x_posting_template.csv` … スケジュール CSV に追加推奨の列例

CSV に追加推奨の列:
- `note_url` … 公開済みの note 記事 URL（必須）
- `hashtags` … カンマ区切り（例: `#損回避,#裏ワザ,#300円note`）
- `image_path` … 画像パス（任意。あれば添付）
- `thread_2`, `thread_3` … スレッド 2-3 本目の文面（任意）。空なら単発のみ

> 既存の `tracking_sheet.csv` は残したまま運用できます。上記列を右端に追記してください。

---

## セットアップ手順（5分）

1. n8n を起動（既存の `workflows/docker-compose.yml` を流用可）
2. n8n UI 右上「Import from File」から `workflows/x-gethnote-auto-poster.json` をインポート
3. ノードの Credentials を作成
   - OpenAI: API Key（`gpt-4o-mini` 推奨）
   - Twitter（X）: API Key/Secret + Access Token/Secret（Elevated 以上の権限が必要）
4. `Read CSV` ノードのパスを自環境に合わせて変更:
   - 例: `C:\\Repos\\note-articles\\gethnote\\schedule\\tracking_sheet.csv`
5. テスト実行（当該時間に近い行がない場合は、CSV の `日付/配信時刻` を直近にして試す）
6. 問題なければワークフローを Active にする

---

## カスタマイズ（推奨）

- 投稿頻度: Cron を「毎 5 分 → 毎 1 分」などへ調整
- 時刻判定幅: Function ノードの ±8 分を環境に合わせて変更
- テンプレ: OpenAI ノードのシステム/ユーザープロンプトを `gethnote/prompt/geth_prompt.txt` から安全版に最適化
- 画像最適化: `tools/image_optimizer.py` で 16:9 / 1080×608 に整形後に添付
- スレッド: `thread_2/3` が埋まっていれば連投。空なら単発

---

## セーフティとポリシー

- 侮蔑・差別・わいせつ・暴力的表現、虚偽の社会的証明などは禁止
- 金融/医療を断定する表現は避け、一般情報か自己責任のディスクレーマを付す
- クリック誘導は「一次情報への明確なリンク（note_url）」を必須
- ハッシュタグは 2-4 個に抑え、露骨なセンシティブタグは使用しない

ワークフロー内に:
- OpenAI でのポリシーフィルタ
- 最終テキストの簡易 NG ワード除去
を入れてあります。必要に応じて語彙リストを拡張してください。

---

## 運用 Tips（GETHNOTE に最適化）

- 朝/昼/夜の 3 枠に対して、テーマを A/B/C でローテし、CTR が高い型を週次で固定化
- `tracking_sheet.csv` に CTR/購入率を週次集計 → 次週のカテゴリ配分を調整
- `note_url` は UTM を必ず付与（例: `?utm_source=x&utm_medium=social&utm_campaign=gethnote`）
- スレッド 2 本目は「裏側の1行チラ見せ」、3 本目は「価格錨＋損失回避」など役割分担

---

## 既知の制約

- ローカル CSV の上書き更新は環境依存です。まずは `posted.json` に二重投稿防止キーを保存し、CSV 更新は手動でも運用可能です
- `n8n-nodes-fs` を使うと CSV 追記やファイル存在チェックが楽になります（任意導入）

---

## 次のステップ

- すぐ試す場合は、`tracking_sheet.csv` の先頭 1 行に直近の日時と `note_url` を入れて Active にしてください
- うまく動いたら、`hashtags` と `image_path` を埋めてリッチ化 → 3 本/日の自動化へ拡大

---

疑問点や追加したい機能（自動リプ/引用RT/コメント抽出など）があれば、この README に沿って拡張します。
