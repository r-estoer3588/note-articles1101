# X API v2 運用分析ツール セットアップガイド

## 前提条件

- Python 3.10以上
- X Developer Account（無料でも可）
- VSCode または任意のPythonエディタ

---

## 1. X API v2 の認証情報取得

### 1.1 開発者アカウント登録

1. [X Developer Portal](https://developer.x.com/en/portal/dashboard) にアクセス
2. 「Sign up」から開発者アカウント作成
3. 使用目的を記入（例: "個人のSNS運用分析のため"）
4. 承認を待つ（通常1〜2日）

### 1.2 プロジェクト・アプリ作成

1. Developer Portal にログイン
2. 「Projects & Apps」→「Create Project」
3. プロジェクト名: `x-operation-analyzer`
4. Use case: `Making a bot`
5. App name: `analyzer-app`
6. **Bearer Token** が表示される → **必ず保存**

---

## 2. ローカル環境構築

### 2.1 リポジトリ準備

```powershell
# プロジェクトディレクトリ作成
cd C:\Repos\note-articles
mkdir -p tools/x-analyzer
cd tools/x-analyzer

# 仮想環境作成（推奨）
python -m venv venv
.\venv\Scripts\Activate.ps1

# 必要なライブラリインストール
pip install tweepy pandas matplotlib seaborn python-dotenv openpyxl
```

### 2.2 認証情報設定

`.env` ファイルを作成:

```env
# X API v2 Bearer Token
X_BEARER_TOKEN=your_bearer_token_here

# アカウント情報（分析対象）
AI_NARRATIVE_USERNAME=your_ai_narrative_username
AI_NARRATIVE_FOLLOWERS=500

GETHNOTE_USERNAME=your_gethnote_username
GETHNOTE_FOLLOWERS=200
```

**⚠️ 重要**: `.env` は `.gitignore` に追加（公開厳禁）

---

## 3. スクリプトの使い方

### 3.1 基本的な実行

```powershell
# AI Narrative Studio の分析
python x_api_analyzer.py
```

実行すると以下が生成されます:

```
./reports/
├── 20251108_120000_AI_Narrative_Studio_summary.csv
├── 20251108_120000_AI_Narrative_Studio_media_analysis.csv
├── 20251108_120000_AI_Narrative_Studio_time_analysis.csv
├── 20251108_120000_AI_Narrative_Studio_top_tweets.csv
└── 20251108_120000_AI_Narrative_Studio_heatmap.png
```

### 3.2 カスタム分析例

```python
from x_api_analyzer import XAnalyzer
import os
from dotenv import load_dotenv

load_dotenv()
analyzer = XAnalyzer(os.getenv('X_BEARER_TOKEN'))

# 過去7日間のデータ取得
from datetime import datetime, timedelta
df = analyzer.fetch_user_tweets(
    username='your_username',
    max_results=50,
    start_time=datetime.utcnow() - timedelta(days=7)
)

# メディア別分析
print(analyzer.analyze_by_media_type(df))

# トップ5投稿
print(analyzer.get_top_tweets(df, metric='like_count', top_n=5))
```

---

## 4. 自動化設定（月次レポート）

### 4.1 Windows タスクスケジューラ

1. `run_monthly_report.ps1` を作成:

```powershell
# PowerShellスクリプト
cd C:\Repos\note-articles\tools\x-analyzer
.\venv\Scripts\Activate.ps1
python x_api_analyzer.py
deactivate

# メール通知（オプション）
Send-MailMessage -To "your@email.com" `
    -From "analyzer@yourdomain.com" `
    -Subject "月次X分析レポート完了" `
    -Body "レポートが生成されました" `
    -SmtpServer "smtp.gmail.com"
```

2. タスクスケジューラに登録:
   - トリガー: 毎月1日 午前6時
   - 操作: `powershell.exe -File "C:\Repos\note-articles\tools\x-analyzer\run_monthly_report.ps1"`

### 4.2 GitHub Actions（クラウド自動化）

`.github/workflows/x-analysis.yml`:

```yaml
name: X API Monthly Analysis

on:
  schedule:
    - cron: '0 6 1 * *'  # 毎月1日 6:00 UTC
  workflow_dispatch:  # 手動実行も可能

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install tweepy pandas matplotlib seaborn python-dotenv
      
      - name: Run analysis
        env:
          X_BEARER_TOKEN: ${{ secrets.X_BEARER_TOKEN }}
        run: |
          python tools/x-analyzer/x_api_analyzer.py
      
      - name: Upload reports
        uses: actions/upload-artifact@v3
        with:
          name: x-analysis-reports
          path: tools/x-analyzer/reports/
```

**Secrets設定**:
- GitHub リポジトリ → Settings → Secrets → New repository secret
- Name: `X_BEARER_TOKEN`
- Value: あなたのBearer Token

---

## 5. トラブルシューティング

### Q1: `401 Unauthorized` エラー

**原因**: Bearer Tokenが無効

**解決策**:
1. Developer Portalで新しいトークン再生成
2. `.env` を更新
3. アプリの権限設定を確認（Read-only でOK）

### Q2: `429 Too Many Requests` エラー

**原因**: レート制限超過

**解決策**:
- Freeプラン: 15分ごとに15リクエストまで
- 取得間隔を空ける（`time.sleep(60)`）
- Basicプランへのアップグレード検討

### Q3: 日本語が文字化け

**原因**: Windowsのデフォルトエンコーディング

**解決策**:
```python
# CSVファイル保存時
df.to_csv('output.csv', encoding='utf-8-sig')
```

### Q4: グラフが表示されない

**原因**: 日本語フォント未設定

**解決策**:
```python
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['MS Gothic']  # Windows
# または
plt.rcParams['font.sans-serif'] = ['Hiragino Sans']  # Mac
```

---

## 6. 次のステップ

### Phase 1: データ蓄積（1〜3ヶ月）

- [ ] 週1回の手動実行で慣れる
- [ ] 投稿に「テーマタグ」を手動で追加
- [ ] 月次レポートを見て傾向を把握

### Phase 2: 高度な分析（4〜6ヶ月）

- [ ] 感情分析の追加（`transformers` ライブラリ）
- [ ] 競合アカウントの自動取得
- [ ] ダッシュボード化（Streamlit）

### Phase 3: 予測・自動化（7〜12ヶ月）

- [ ] 機械学習での「高ERになる投稿」予測
- [ ] 投稿の自動スケジューリング
- [ ] 異常検知アラート（ER急落・炎上）

---

## 7. 参考リソース

- [X API v2 公式ドキュメント](https://developer.x.com/en/docs/twitter-api)
- [tweepy ドキュメント](https://docs.tweepy.org/en/stable/)
- [pandas チートシート](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)

---

## 8. サポート・質問

問題が発生した場合:
1. エラーメッセージを確認
2. [X API Status](https://api.twitterstat.us/) でサービス状態確認
3. GitHub Issuesに報告（このリポジトリの場合）

---

**重要**: このツールは「分析」が目的です。**投稿の自動化・大量フォロー・スパム的な使用は規約違反**となり、アカウント凍結のリスクがあります。節度を持って使用してください。
