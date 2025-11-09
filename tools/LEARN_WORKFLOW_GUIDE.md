# 学習機能ワークフロー実装ガイド

## 概要
LINE Bot の「学習」メニューから、過去の投稿データを分析してテンプレート精度を向上させる機能を実装しました。

**✨ 新機能追加（v2）**:
- **進捗通知**: 学習途中の経過をLINE pushで通知（20%刻み）
- **定期自動学習**: 毎週日曜 3:00 AM に自動実行

---

## 追加したノード（n8n_workflow_menu_complete.json）

### 手動実行フロー（リッチメニュー経由）

#### 1. 学習確認表示分岐（switch-action-learn-confirm）
- **ID**: `switch-action-learn-confirm`
- **位置**: [1050, 600]
- **トリガー条件**: `nextAction === 'show_learn_confirm'`
- **役割**: リッチメニュー「学習」タップ時の確認メッセージ表示分岐

### 2. 学習確認メッセージ作成（create-learn-confirm-message）
- **ID**: `create-learn-confirm-message`
- **位置**: [1250, 600]
- **メッセージ内容**:
  ```
  🎓 学習を実行しますか？
  
  学習内容:
  ・過去の投稿データを分析
  ・バズりやすいパターンを学習
  ・テンプレートの精度を向上
  
  所要時間: 約3〜5分
  ```
- **QuickReply**:
  - ✅ 実行する → postback `action=learn_execute`
  - ❌ キャンセル → テキスト `キャンセル`

### 3. 学習実行分岐（switch-action-learn-exec）
- **ID**: `switch-action-learn-exec`
- **位置**: [1050, 700]
- **トリガー条件**: `nextAction === 'execute_learn'`
- **役割**: ポストバック `learn_execute` 受信時の実行分岐

### 4. 学習ローディングメッセージ（create-learn-loading）
- **ID**: `create-learn-loading`
- **位置**: [1250, 700]
- **メッセージ内容**:
  ```
  🎓 学習を開始します...
  ⏳ 3〜5分お待ちください
  ```

### 5. 学習スクリプト実行（execute-learn-script）
- **ID**: `execute-learn-script`
- **位置**: [1450, 720]
- **コマンド**:
  ```bash
  cd c:\Repos\note-articles\tools && python hogey_algorithm.py --learn --input my_posts_sample.csv
  ```
- **処理内容**:
  - `hogey_algorithm.py` を学習モードで実行
  - 入力: `my_posts_sample.csv`（過去の投稿データ）
  - 出力: 学習済みモデル/テンプレート更新

### 6. 学習結果メッセージ作成（create-learn-result-message）
- **ID**: `create-learn-result-message`
- **位置**: [1650, 720]
- **処理ロジック**:
  - `exitCode === 0` → 成功メッセージ（stdout の最後3行を要約表示）
  - `exitCode !== 0` → 失敗メッセージ（stderr の最初3行を表示）

## 接続フロー

```
状態判定 → 学習確認表示? → 学習確認メッセージ作成 → LINE返信
         ↓
         学習実行? → 学習ローディング → LINE返信
                                     ↓
                                     学習スクリプト実行 → 学習結果メッセージ作成 → LINE返信
```

## 使用方法

### ユーザー操作フロー
1. LINEリッチメニューで「🎓 学習」をタップ
2. 確認メッセージを受信
3. 「✅ 実行する」をタップ
4. ローディングメッセージ受信
5. 3〜5分待機
6. 完了メッセージ受信（成功 or 失敗）

### 学習スクリプトの前提条件
- **ファイル存在**: `c:\Repos\note-articles\tools\my_posts_sample.csv`
- **Python環境**: hogey_algorithm.py が動作する仮想環境（venv等）
- **引数サポート**: `--learn --input <CSV>` オプション実装済み

### カスタマイズポイント

#### 1. 入力CSV変更
```javascript
// execute-learn-script の command パラメータを編集
"command": "cd c:\\Repos\\note-articles\\tools && python hogey_algorithm.py --learn --input YOUR_CSV.csv"
```

#### 2. 所要時間調整
```javascript
// create-learn-confirm-message の text 内容を変更
text: '所要時間: 約X〜Y分'
```

#### 3. 結果メッセージの詳細度
```javascript
// create-learn-result-message で表示行数を調整
const summary = lines.slice(-3).join('\\n');  // 最後3行 → 任意の行数へ
```

## エラーハンドリング

### よくあるエラーと対処

| エラーパターン | 原因 | 対処 |
|------------|------|------|
| exitCode != 0 | CSVファイルが存在しない | my_posts_sample.csv の配置確認 |
| exitCode != 0 | Python環境エラー | venv 有効化確認、依存パッケージインストール |
| タイムアウト | 処理時間超過 | n8n のコマンド実行タイムアウト設定を延長 |
| stderr に "No module" | パッケージ未インストール | `pip install -r requirements.txt` |

### n8n タイムアウト設定
Execute Command ノードのデフォルトタイムアウトは 60秒。学習処理が長い場合は延長:
```json
{
  "parameters": {
    "command": "...",
    "timeout": 600  // 10分に延長
  }
}
```

## 検証手順

### 1. JSON構文チェック
```powershell
Get-Content -Raw 'c:\Repos\note-articles\tools\n8n_workflow_menu_complete.json' | ConvertFrom-Json | Out-Null
Write-Host 'OK'
```

### 2. 学習スクリプト単体テスト
```powershell
cd c:\Repos\note-articles\tools
python hogey_algorithm.py --learn --input my_posts_sample.csv
```

### 3. n8n 動作確認
1. n8n にワークフローをインポート
2. LINE Webhook を設定
3. リッチメニューに「学習」ボタンを配置（`menu:learn` テキスト送信）
4. 実際にLINEから操作して動作確認

## 今後の拡張案

- **進捗通知**: 学習途中経過を push メッセージで通知
- **スケジュール学習**: cron で定期自動学習
- **学習履歴**: Google Sheets に実行履歴・精度変化を記録
- **複数モデル**: バズ用/ストーリー用など目的別学習
- **A/Bテスト**: 学習前後の投稿パフォーマンス比較

## 参考

- メインワークフロー: `n8n_workflow_menu_complete.json`
- 学習スクリプト: `hogey_algorithm.py`
- 正規化スクリプト: `normalize_facts.py`
- データセット: `data_collection_output.json`
