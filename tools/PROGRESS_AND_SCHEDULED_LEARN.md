# 進捗通知＆定期自動学習 実装完了レポート

## 実装概要
LINE Bot の学習機能に以下2つの機能を追加しました:
1. **進捗通知**: 学習中の進捗（%）をLINE pushで通知
2. **定期自動学習**: 毎週日曜 3:00 AM に自動実行

---

## 1. 進捗通知機能

### 実装内容

#### A. 学習スクリプトの変更（hogey_algorithm.py）
`learn_from_csv` メソッドに進捗出力を追加:
- 開始時: `PROGRESS:0:TOTAL`
- 処理中: `PROGRESS:XX:TOTAL`（各投稿分析後）
- 完了時: `PROGRESS:100:TOTAL`

**変更箇所**:
- Line 112-195: 進捗計算ロジック追加
- 20〜30件の投稿を分析する際、各件ごとに進捗%を算出して出力

#### B. 進捗通知ラッパー（learn_with_progress_push.py）新規作成
`hogey_algorithm.py` をサブプロセスで実行し、stdout をリアルタイム監視:
- `PROGRESS:XX:TOTAL` 形式を検出
- 20%刻み（0%, 20%, 40%, 60%, 80%, 100%）でLINE push通知
- 完了時に成功/失敗の最終メッセージを送信

**環境変数**:
- `LINE_CHANNEL_ACCESS_TOKEN`: LINEチャネルアクセストークン
- `LINE_USER_ID`: 通知先ユーザーID（管理者）

**通知メッセージ例**:
```
🎓 学習進捗: 20%
処理中: 50件

🎓 学習進捗: 40%
処理中: 50件

...

✅ 学習が完了しました！
次回の投稿生成から新しいパターンが反映されます。
```

---

## 2. 定期自動学習機能

### 実装内容

#### A. n8n ノード追加

##### 1. 定期学習トリガー（cron-weekly-learn）
- **タイプ**: Schedule Trigger
- **スケジュール**: `0 3 * * 0`（毎週日曜 3:00 AM）
- **位置**: [250, 900]

##### 2. 定期学習開始通知（create-scheduled-learn-start-push）
- **タイプ**: Code
- **位置**: [650, 900]
- **機能**: 管理者へ開始通知メッセージを作成
- **メッセージ**:
  ```
  🎓 定期学習を開始しました
  完了まで3〜5分お待ちください
  ```

##### 3. LINE Push（定期）（line-push-scheduled）
- **タイプ**: HTTP Request
- **位置**: [850, 900]
- **機能**: 管理者に開始通知を送信

##### 4. 学習実行（進捗通知付き）（execute-learn-with-progress）
- **タイプ**: Execute Command
- **位置**: [450, 920]
- **コマンド**:
  ```powershell
  cd c:\Repos\note-articles\tools && 
  set LINE_CHANNEL_ACCESS_TOKEN={{ $env.LINE_CHANNEL_ACCESS_TOKEN }} && 
  set LINE_USER_ID={{ $env.ADMIN_LINE_USER_ID }} && 
  python learn_with_progress_push.py --learn --input my_posts_sample.csv
  ```

#### B. 接続フロー
```
定期学習トリガー（毎週日曜 3:00）
  ↓
定期学習開始通知 ──→ LINE Push（定期）─→ （管理者に通知）
  ↓
学習実行（進捗通知付き）
  ↓（20%刻みで自動push）
  📱 "🎓 学習進捗: 20%"
  📱 "🎓 学習進捗: 40%"
  📱 "🎓 学習進捗: 60%"
  📱 "🎓 学習進捗: 80%"
  📱 "✅ 学習が完了しました！"
```

---

## セットアップ手順

### 1. 環境変数の設定（n8n）
n8n の環境変数に以下を追加:
```bash
LINE_CHANNEL_ACCESS_TOKEN=your_channel_access_token
ADMIN_LINE_USER_ID=U1234567890abcdef  # 管理者のLINE USER ID
```

### 2. ファイル配置確認
```
c:\Repos\note-articles\tools\
├── hogey_algorithm.py               # 進捗出力追加済み
├── learn_with_progress_push.py      # 新規作成
├── my_posts_sample.csv              # 学習用データ
└── n8n_workflow_menu_complete.json  # 更新済み
```

### 3. n8n ワークフロー更新
1. n8n管理画面にログイン
2. 既存ワークフローを開く
3. `n8n_workflow_menu_complete.json` をインポート（上書き）
4. 環境変数が反映されていることを確認

### 4. 動作確認

#### 手動実行テスト
```powershell
cd c:\Repos\note-articles\tools
python learn_with_progress_push.py --learn --input my_posts_sample.csv
```
→ 進捗が20%刻みで出力されることを確認

#### n8n テスト
1. n8n で「定期学習トリガー」ノードを手動実行
2. 管理者LINEに開始通知が届くことを確認
3. 20%刻みで進捗通知が届くことを確認
4. 完了通知が届くことを確認

---

## スケジュール調整

### Cron 式の変更方法
定期学習トリガーノードの `cronExpression` を編集:

| スケジュール | Cron式 | 説明 |
|------------|--------|------|
| 毎週日曜 3:00 AM | `0 3 * * 0` | デフォルト |
| 毎日 2:00 AM | `0 2 * * *` | 毎日実行 |
| 毎週月曜 0:00 AM | `0 0 * * 1` | 週初め実行 |
| 毎月1日 4:00 AM | `0 4 1 * *` | 月初め実行 |

**編集箇所**（n8n_workflow_menu_complete.json）:
```json
{
  "parameters": {
    "rule": {
      "interval": [
        {
          "field": "cronExpression",
          "expression": "0 3 * * 0"  ← ここを変更
        }
      ]
    }
  },
  "id": "cron-weekly-learn",
  "name": "定期学習トリガー"
}
```

---

## トラブルシューティング

### 進捗通知が届かない
**原因**: 環境変数が未設定 or LINE_USER_ID が間違っている

**対処**:
1. n8n環境変数を確認:
   ```bash
   echo $env:LINE_CHANNEL_ACCESS_TOKEN
   echo $env:ADMIN_LINE_USER_ID
   ```
2. LINE USER IDの取得方法:
   - LINEで任意のメッセージを送信
   - Webhook イベントの `source.userId` をログで確認

### 学習が途中で止まる
**原因**: CSVファイルが壊れている or Python環境エラー

**対処**:
```powershell
# 単体テスト
cd c:\Repos\note-articles\tools
python hogey_algorithm.py --learn --input my_posts_sample.csv

# エラーログ確認
# n8n の Execute Command ノードの stderr を確認
```

### 定期実行が動かない
**原因**: n8n が起動していない or トリガーが無効

**対処**:
1. n8n プロセス確認:
   ```powershell
   Get-Process -Name n8n
   ```
2. n8n 起動:
   ```powershell
   cd C:\path\to\n8n
   n8n
   ```
3. ワークフロー画面で「Active」トグルがONになっていることを確認

---

## 今後の拡張案

### 1. 進捗通知の詳細化
- 現在の処理フェーズを表示（例: 「自分の投稿を分析中...」）
- 推定残り時間を計算して通知

### 2. 学習結果の可視化
- 学習前後のスコア比較
- 新たに学習したキーワードTOP10をメッセージで送信

### 3. 複数モデル対応
- バズ用/ストーリー用でモデルを分離
- カテゴリ別に学習スケジュールを設定

### 4. エラー時の自動リトライ
- 失敗時に10分後に再実行
- 3回失敗したら管理者に緊急通知

### 5. 学習履歴の記録
- Google Sheets に実行日時、処理件数、成功/失敗を記録
- ダッシュボードで可視化

---

## 更新ファイル一覧

### 変更
- `c:\Repos\note-articles\tools\hogey_algorithm.py`
  - `learn_from_csv` メソッドに進捗出力追加

- `c:\Repos\note-articles\tools\n8n_workflow_menu_complete.json`
  - 定期学習トリガーノード追加
  - 定期学習開始通知ノード追加
  - LINE Push（定期）ノード追加
  - 学習実行（進捗通知付き）ノード追加
  - 接続フロー更新

### 新規
- `c:\Repos\note-articles\tools\learn_with_progress_push.py`
  - 進捗通知ラッパースクリプト

- `c:\Repos\note-articles\tools\PROGRESS_AND_SCHEDULED_LEARN.md`
  - 本ドキュメント

---

## 検証ステータス
- ✅ hogey_algorithm.py の進捗出力実装
- ✅ learn_with_progress_push.py 作成
- ✅ n8n ノード追加（定期トリガー、進捗通知）
- ✅ JSON構文検証（OK）
- ⏳ 実機テスト（環境変数設定後に実施）

---

## まとめ
進捗通知と定期自動学習の実装により、以下が実現:
1. **ユーザー体験向上**: 学習中の進捗が可視化され、安心して待てる
2. **運用自動化**: 毎週自動で学習が実行され、常に最新のパターンで投稿生成
3. **管理者の負担軽減**: 手動実行不要、異常時のみ通知で確認

次のステップは実機テストと、必要に応じて通知頻度・スケジュールの調整です。
