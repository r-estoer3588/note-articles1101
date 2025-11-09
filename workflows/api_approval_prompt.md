# X API 承認後の初期セットアップ プロンプト

このプロンプトをGitHub Copilot Chatにコピペしてください。

---

## 📋 プロンプト本文（ここからコピー）

```
X API v2の承認が来ました。これから以下を順番に実行したいです：

1. X Developer Portalでの設定確認とBearer Token取得手順
2. .envファイルの作成と設定
3. 初回データ取得テスト（自分の過去30日の投稿データ）
4. レポート生成と結果確認
5. 今後の運用フローの確認

環境情報：
- リポジトリ: C:\Repos\note-articles
- Python環境: C:\Repos\note-articles\tools\venv（作成済み）
- 分析スクリプト: C:\Repos\note-articles\tools\x_api_analyzer.py（作成済み）
- ドキュメント:
  - C:\Repos\note-articles\designs\x_api_operation_framework.md
  - C:\Repos\note-articles\designs\ai_narrative_studio_operation_manual.md
  - C:\Repos\note-articles\tools\x_api_setup_guide.md

アカウント情報：
- AI Narrative Studio: [あなたのユーザー名を記入]
- GETHNOTE: [あなたのユーザー名を記入]

1つずつ手順を教えてください。PowerShellコマンドとブラウザ操作の両方で案内をお願いします。
```

---

## 🎯 プロンプト使用時の注意

### 事前に準備しておくこと
- [ ] X Developer Portalにログインできる状態
- [ ] 自分のXユーザー名を確認（@なし）
- [ ] 現在のフォロワー数を確認

### プロンプトに追加で記入すること
```
アカウント情報：
- AI Narrative Studio: your_actual_username  ← ここを実際のユーザー名に
- GETHNOTE: your_gethnote_username          ← ここも実際のユーザー名に
```

### プロンプトを投げる前にやること
```powershell
# ターミナルを開いて以下を実行
cd C:\Repos\note-articles\tools
.\venv\Scripts\Activate.ps1
```

---

## 📝 補足：よくある質問への回答も含めたプロンプト（詳細版）

詳しく聞きたい場合は、こちらのバージョンを使ってください：

```
X API v2の承認が来ました。初回セットアップを段階的にサポートしてください。

## 現在の状況
- X Developer Accountの承認完了（メール受信済み）
- Python環境: C:\Repos\note-articles\tools\venv（構築済み、ライブラリインストール済み）
- 分析スクリプト: x_api_analyzer.py（作成済み）
- .envテンプレート: .env.template（作成済み）

## やりたいこと（順番に）
### Phase 1: Bearer Token取得（今すぐ）
1. X Developer PortalでどこからBearer Tokenを取得するか
2. Tokenの安全な保存方法
3. .envファイルへの設定手順

### Phase 2: 初回データ取得テスト（Phase 1の直後）
1. 自分の過去投稿データ取得（AI Narrative Studio）
2. エラーが出た場合のトラブルシューティング
3. レポートファイルの確認方法

### Phase 3: 分析結果の読み方（Phase 2の直後）
1. 生成されたCSVファイルの見方
2. ヒートマップの解釈
3. 「勝ちパターン」の見つけ方

### Phase 4: 週次運用の設計（Phase 3の後）
1. 毎週日曜夜にやるべきこと
2. 月次レポートの生成方法
3. 投稿計画への反映方法

## アカウント情報
- AI Narrative Studio: [ユーザー名]、フォロワー: [数]
- GETHNOTE: [ユーザー名]、フォロワー: [数]

## 質問・懸念点
- Bearer Tokenを間違えて公開しないか心配
- APIのレート制限に引っかからないか
- 最初の分析で何を見ればいいかわからない

各Phaseごとに、次に進む前に確認をお願いします。
PowerShellコマンド、ブラウザ操作、VSCode操作を具体的に指示してください。
```

---

## 🚀 承認後の予想タイムライン

| 時間 | アクション | 所要時間 |
|------|-----------|---------|
| 0分 | プロンプトをコピペ | 1分 |
| 1分 | Bearer Token取得ガイド受け取り | - |
| 2分 | Developer Portalで取得 | 5分 |
| 7分 | .envファイル設定 | 3分 |
| 10分 | 初回データ取得実行 | 2分 |
| 12分 | レポート生成待ち | 1分 |
| 13分 | 結果確認＆解釈 | 10分 |
| 23分 | 週次運用フロー確認 | 5分 |
| **合計** | **約30分で運用開始可能** | - |

---

## 📁 このプロンプトファイルの保存場所

- ファイル: `C:\Repos\note-articles\workflows\api_approval_prompt.md`
- いつでも参照可能
- 承認メールが来たらすぐコピペ

---

## 🔖 ブックマーク推奨

承認メールが来たら：
1. このファイルを開く
2. 「プロンプト本文」セクションをコピー
3. GitHub Copilot Chatに貼り付け
4. ユーザー名とフォロワー数を記入
5. 送信

以上です！準備万端🎉
